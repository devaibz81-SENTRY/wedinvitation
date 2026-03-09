import { internalQuery, internalMutation } from "./_generated/server";
import { v } from "convex/values";

const attendanceValidator = v.union(
  v.literal("invited"),
  v.literal("attending"),
  v.literal("declined"),
  v.literal("later")
);

const rsvpAttendanceValidator = v.union(
  v.literal("attending"),
  v.literal("declined"),
  v.literal("later")
);

function normalizeWhitespace(value: string) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, " ");
}

function makeNameKey(firstName: string, lastName: string) {
  return `${normalizeWhitespace(firstName)} ${normalizeWhitespace(lastName)}`.trim();
}

function normalizePhone(phone?: string) {
  const digits = String(phone || "").replace(/[^\d]/g, "");
  return digits.length ? digits : undefined;
}

export const list = internalQuery({
  args: {},
  handler: async (ctx) => {
    const guests = await ctx.db.query("guests").collect();
    return guests.sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
  },
});

export const add = internalMutation({
  args: {
    first_name: v.string(),
    last_name: v.string(),
    guest_type: v.union(v.literal("single"), v.literal("couple"), v.literal("family")),
    max_party: v.number(),
    phone: v.optional(v.string()),
    email: v.optional(v.string()),
    deadline: v.optional(v.string()),
    attendance: v.optional(attendanceValidator),
  },
  handler: async (ctx, args) => {
    const now = new Date().toISOString();
    const nameKey = makeNameKey(args.first_name, args.last_name);
    const phoneKey = normalizePhone(args.phone);

    let existing = null;
    let dedupedBy: "phone" | "name" | null = null;

    if (phoneKey) {
      existing = await ctx.db
        .query("guests")
        .withIndex("by_phone_key", (q) => q.eq("phone_key", phoneKey))
        .first();
      if (existing) dedupedBy = "phone";
    }

    if (!existing) {
      existing = await ctx.db
        .query("guests")
        .withIndex("by_name_key", (q) => q.eq("name_key", nameKey))
        .first();
      if (existing) dedupedBy = "name";
    }

    if (existing) {
      const requestedAttendance = args.attendance ?? "invited";
      const nextAttendance =
        existing.attendance !== "invited" && requestedAttendance === "invited"
          ? existing.attendance
          : requestedAttendance;

      await ctx.db.patch(existing._id, {
        first_name: args.first_name,
        last_name: args.last_name,
        name_key: nameKey,
        guest_type: args.guest_type,
        max_party: args.max_party,
        phone: args.phone,
        phone_key: phoneKey,
        email: args.email,
        deadline: args.deadline,
        attendance: nextAttendance,
        updated_at: now,
      });

      return { id: existing._id, updated: true, dedupedBy };
    }

    const id = await ctx.db.insert("guests", {
      ...args,
      name_key: nameKey,
      phone_key: phoneKey,
      attendance: args.attendance ?? "invited",
      created_at: now,
      updated_at: now,
    });
    return { id, created: true };
  },
});

export const updateFromRsvp = internalMutation({
  args: {
    guestId: v.optional(v.id("guests")),
    first_name: v.string(),
    last_name: v.string(),
    email: v.string(),
    phone: v.optional(v.string()),
    attendance: rsvpAttendanceValidator,
    guest_type: v.optional(v.string()),
    message: v.optional(v.string()),
    submitted_at: v.string(),
  },
  handler: async (ctx, args) => {
    const now = new Date().toISOString();
    const submittedNameKey = makeNameKey(args.first_name, args.last_name);
    const submittedPhoneKey = normalizePhone(args.phone);

    const logGateQuery = async (reason: "name_mismatch" | "guest_not_found" | "ambiguous_name", expectedName?: string) => {
      await ctx.db.insert("rsvp_gate_queries", {
        guest_id: args.guestId,
        submitted_first_name: args.first_name,
        submitted_last_name: args.last_name,
        submitted_email: args.email || undefined,
        submitted_phone: args.phone,
        attendance: args.attendance,
        reason,
        expected_name: expectedName,
        created_at: now,
        status: "open",
      });
    };

    let targetGuest = args.guestId ? await ctx.db.get(args.guestId) : null;

    if (args.guestId && !targetGuest) {
      await logGateQuery("guest_not_found");
      return { guestId: null, rejected: true, reason: "guest_not_found" };
    }

    if (!targetGuest && submittedPhoneKey) {
      targetGuest = await ctx.db
        .query("guests")
        .withIndex("by_phone_key", (q) => q.eq("phone_key", submittedPhoneKey))
        .first();
    }

    if (!targetGuest && args.email) {
      targetGuest = await ctx.db
        .query("guests")
        .withIndex("by_email", (q) => q.eq("email", args.email))
        .first();
    }

    if (!targetGuest) {
      const sameNameGuests = await ctx.db
        .query("guests")
        .withIndex("by_name_key", (q) => q.eq("name_key", submittedNameKey))
        .collect();
      if (sameNameGuests.length === 1) {
        targetGuest = sameNameGuests[0];
      } else if (sameNameGuests.length > 1) {
        await logGateQuery("ambiguous_name");
        return { guestId: null, rejected: true, reason: "ambiguous_name" };
      }
    }

    if (!targetGuest) {
      await logGateQuery("guest_not_found");
      return { guestId: null, rejected: true, reason: "guest_not_found" };
    }

    const expectedNameKey = targetGuest.name_key ?? makeNameKey(targetGuest.first_name, targetGuest.last_name);
    const expectedName = `${targetGuest.first_name} ${targetGuest.last_name}`.trim();
    if (expectedNameKey !== submittedNameKey) {
      await logGateQuery("name_mismatch", expectedName);
      return {
        guestId: null,
        rejected: true,
        reason: "name_mismatch",
        expectedName,
      };
    }

    const nextPhone = args.phone ?? targetGuest.phone;
    const nextPhoneKey = normalizePhone(nextPhone);
    const nextEmail = targetGuest.email ?? args.email;

    await ctx.db.patch(targetGuest._id, {
      first_name: targetGuest.first_name,
      last_name: targetGuest.last_name,
      name_key: expectedNameKey,
      email: nextEmail,
      phone: nextPhone,
      phone_key: nextPhoneKey,
      attendance: args.attendance,
      message: args.message,
      submitted_at: args.submitted_at,
      updated_at: now,
    });

    return { guestId: targetGuest._id, rejected: false };
  },
});

export const listGateQueries = internalQuery({
  args: {
    status: v.optional(v.union(v.literal("open"), v.literal("resolved"))),
  },
  handler: async (ctx, args) => {
    const rows = args.status
      ? await ctx.db
          .query("rsvp_gate_queries")
          .withIndex("by_status", (q) => q.eq("status", args.status!))
          .collect()
      : await ctx.db.query("rsvp_gate_queries").collect();
    return rows.sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
  },
});

export const remove = internalMutation({
  args: {
    guestId: v.id("guests"),
  },
  handler: async (ctx, args) => {
    const existing = await ctx.db.get(args.guestId);
    if (!existing) {
      return { deleted: false };
    }

    // Clean up linked RSVPs for this guest to keep admin data consistent.
    const rsvps = await ctx.db.query("rsvps").collect();
    let removedRsvps = 0;
    for (const rsvp of rsvps) {
      if (rsvp.guest_id === args.guestId) {
        await ctx.db.delete(rsvp._id);
        removedRsvps += 1;
      }
    }

    await ctx.db.delete(args.guestId);
    return { deleted: true, removedRsvps };
  },
});
