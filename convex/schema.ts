import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  guests: defineTable({
    first_name: v.string(),
    last_name: v.string(),
    guest_type: v.union(v.literal("single"), v.literal("couple"), v.literal("family")),
    max_party: v.number(),
    phone: v.optional(v.string()),
    email: v.optional(v.string()),
    deadline: v.optional(v.string()),
    attendance: v.union(
      v.literal("invited"),
      v.literal("attending"),
      v.literal("declined"),
      v.literal("later")
    ),
    message: v.optional(v.string()),
    submitted_at: v.optional(v.string()),
    created_at: v.string(),
    updated_at: v.string(),
  })
    .index("by_email", ["email"])
    .index("by_attendance", ["attendance"]),

  rsvps: defineTable({
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
  }).index("by_email", ["email"]),

  admin_sessions: defineTable({
    token: v.string(),
    created_at: v.string(),
    expires_at: v.string(),
  })
    .index("by_token", ["token"])
    .index("by_expires_at", ["expires_at"]),
});
