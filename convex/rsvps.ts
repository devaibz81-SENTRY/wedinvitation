import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const submit = mutation({
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
