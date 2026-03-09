import { internalMutation, internalQuery } from "./_generated/server";
import { v } from "convex/values";

const SESSION_TTL_MS = 1000 * 60 * 60 * 12;

export const createSession = internalMutation({
  args: {
    token: v.string(),
  },
  handler: async (ctx, args) => {
    const now = new Date();
    const createdAt = now.toISOString();
    const expiresAt = new Date(now.getTime() + SESSION_TTL_MS).toISOString();

    await ctx.db.insert("admin_sessions", {
      token: args.token,
      created_at: createdAt,
      expires_at: expiresAt,
    });

    return { expiresAt };
  },
});

export const validateSession = internalQuery({
  args: {
    token: v.string(),
  },
  handler: async (ctx, args) => {
    const row = await ctx.db
      .query("admin_sessions")
      .withIndex("by_token", (q) => q.eq("token", args.token))
      .first();

    if (!row) return { ok: false };
    if (new Date(row.expires_at).getTime() < Date.now()) return { ok: false };
    return { ok: true, expiresAt: row.expires_at };
  },
});

export const revokeSession = internalMutation({
  args: {
    token: v.string(),
  },
  handler: async (ctx, args) => {
    const row = await ctx.db
      .query("admin_sessions")
      .withIndex("by_token", (q) => q.eq("token", args.token))
      .first();

    if (row) {
      await ctx.db.delete(row._id);
    }
    return { ok: true };
  },
});
