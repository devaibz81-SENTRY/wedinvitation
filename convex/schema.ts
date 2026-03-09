import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  guests: defineTable({
    first_name: v.string(),
    last_name: v.string(),
    name_key: v.optional(v.string()),
    guest_type: v.union(v.literal("single"), v.literal("couple"), v.literal("family")),
    max_party: v.number(),
    phone: v.optional(v.string()),
    phone_key: v.optional(v.string()),
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
    .index("by_name_key", ["name_key"])
    .index("by_phone_key", ["phone_key"])
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

  rsvp_gate_queries: defineTable({
    guest_id: v.optional(v.id("guests")),
    submitted_first_name: v.string(),
    submitted_last_name: v.string(),
    submitted_email: v.optional(v.string()),
    submitted_phone: v.optional(v.string()),
    attendance: v.union(v.literal("attending"), v.literal("declined"), v.literal("later")),
    reason: v.union(
      v.literal("name_mismatch"),
      v.literal("guest_not_found"),
      v.literal("ambiguous_name")
    ),
    expected_name: v.optional(v.string()),
    created_at: v.string(),
    status: v.union(v.literal("open"), v.literal("resolved")),
    notes: v.optional(v.string()),
  })
    .index("by_status", ["status"])
    .index("by_reason", ["reason"])
    .index("by_guest_id", ["guest_id"]),
});
