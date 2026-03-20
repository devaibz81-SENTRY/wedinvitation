import { internalMutation, internalQuery, query } from "./_generated/server";
import { v } from "convex/values";

function hasText(value?: string) {
  return String(value ?? "").trim().length > 0;
}

function formatDisplayName(firstName: string, lastName: string) {
  return `${String(firstName || "").trim()} ${String(lastName || "").trim()}`
    .replace(/\s+/g, " ")
    .trim();
}

function sortBySubmittedAtDesc<T extends { submitted_at: string }>(rows: T[]) {
  return [...rows].sort((a, b) => (a.submitted_at < b.submitted_at ? 1 : -1));
}

export const submit = internalMutation({
  args: {
    guest_id: v.optional(v.id("guests")),
    first_name: v.string(),
    last_name: v.string(),
    email: v.string(),
    phone: v.optional(v.string()),
    attendance: v.union(v.literal("attending"), v.literal("declined"), v.literal("later")),
    guest_type: v.optional(v.string()),
    party_names: v.optional(v.string()),
    meal_preference: v.optional(v.string()),
    dietary_requirements: v.optional(v.string()),
    song_request: v.optional(v.string()),
    message: v.optional(v.string()),
    submitted_at: v.string(),
  },
  handler: async (ctx, args) => {
    const id = await ctx.db.insert("rsvps", args);
    return { id };
  },
});

export const listMedia = internalQuery({
  args: {},
  handler: async (ctx) => {
    const rows = sortBySubmittedAtDesc(await ctx.db.query("rsvps").collect());

    const songs = rows
      .filter((row) => hasText(row.song_request))
      .map((row) => ({
        id: row._id,
        display_name: formatDisplayName(row.first_name, row.last_name) || "Guest",
        first_name: row.first_name,
        last_name: row.last_name,
        attendance: row.attendance,
        guest_type: row.guest_type ?? "single",
        song_request: String(row.song_request || "").trim(),
        submitted_at: row.submitted_at,
      }));

    const messages = rows
      .filter((row) => hasText(row.message))
      .map((row) => ({
        id: row._id,
        display_name: formatDisplayName(row.first_name, row.last_name) || "Guest",
        first_name: row.first_name,
        last_name: row.last_name,
        attendance: row.attendance,
        guest_type: row.guest_type ?? "single",
        message: String(row.message || "").trim(),
        submitted_at: row.submitted_at,
      }));

    const uniqueMessageSenders = new Set(
      messages.map((row) => `${row.display_name.toLowerCase()}|${row.first_name.toLowerCase()}|${row.last_name.toLowerCase()}`)
    ).size;

    return {
      songs,
      messages,
      counts: {
        totalRsvps: rows.length,
        songCount: songs.length,
        messageCount: messages.length,
        uniqueMessageSenders,
        lastSubmittedAt: rows[0]?.submitted_at ?? null,
      },
    };
  },
});

export const listMessagesVault = query({
  args: {},
  handler: async (ctx) => {
    const rows = sortBySubmittedAtDesc(await ctx.db.query("rsvps").collect());

    const messages = rows
      .filter((row) => hasText(row.message))
      .map((row) => ({
        id: row._id,
        display_name: formatDisplayName(row.first_name, row.last_name) || "Guest",
        first_name: row.first_name,
        last_name: row.last_name,
        attendance: row.attendance,
        guest_type: row.guest_type ?? "single",
        message: String(row.message || "").trim(),
        submitted_at: row.submitted_at,
      }));

    return {
      messages,
      counts: {
        totalMessages: messages.length,
        lastSubmittedAt: messages[0]?.submitted_at ?? null,
      },
    };
  },
});
