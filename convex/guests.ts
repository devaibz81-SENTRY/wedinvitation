import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

const attendanceValidator = v.union(
  v.literal("invited"),
  v.literal("attending"),
  v.literal("declined"),
  v.literal("later")
);

export const list = query({
  args: {},
  handler: async (ctx) => {
    const guests = await ctx.db.query("guests").collect();
    return guests.sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
  },
});

export const add = mutation({
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
    const id = await ctx.db.insert("guests", {
      ...args,
      attendance: args.attendance ?? "invited",
      created_at: now,
      updated_at: now,
    });
    return { id };
  },
});

export const updateFromRsvp = mutation({
  args: {
    guestId: v.optional(v.id("guests")),
    first_name: v.string(),
    last_name: v.string(),
    email: v.string(),
    phone: v.optional(v.string()),
    attendance: v.union(v.literal("attending"), v.literal("declined"), v.literal("later")),
    guest_type: v.optional(v.string()),
    message: v.optional(v.string()),
    submitted_at: v.string(),
  },
  handler: async (ctx, args) => {
    const now = new Date().toISOString();
    let targetId = args.guestId;

    if (!targetId) {
      const maybeByEmail = await ctx.db
        .query("guests")
        .withIndex("by_email", (q) => q.eq("email", args.email))
        .first();
      targetId = maybeByEmail?._id;
    }

    if (targetId) {
      await ctx.db.patch(targetId, {
        first_name: args.first_name,
        last_name: args.last_name,
        email: args.email,
        phone: args.phone,
        attendance: args.attendance,
        message: args.message,
        submitted_at: args.submitted_at,
        updated_at: now,
      });
    } else {
      const normalizedGuestType =
        args.guest_type === "couple" || args.guest_type === "family"
          ? args.guest_type
          : "single";
      targetId = await ctx.db.insert("guests", {
        first_name: args.first_name,
        last_name: args.last_name,
        guest_type: normalizedGuestType,
        max_party: 1,
        phone: args.phone,
        email: args.email,
        attendance: args.attendance,
        message: args.message,
        submitted_at: args.submitted_at,
        created_at: now,
        updated_at: now,
      });
    }

    return { guestId: targetId ?? null };
  },
});

export const remove = mutation({
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
