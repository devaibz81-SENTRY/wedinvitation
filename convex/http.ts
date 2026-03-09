import { httpRouter } from "convex/server";
import { api } from "./_generated/api";
import { httpAction } from "./_generated/server";
import { Id } from "./_generated/dataModel";

const http = httpRouter();

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
  };
}

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders(),
    },
  });
}

function noContent() {
  return new Response(null, { status: 204, headers: corsHeaders() });
}

function getBearerToken(request: Request) {
  const authHeader = request.headers.get("authorization") ?? "";
  if (!authHeader.startsWith("Bearer ")) return null;
  return authHeader.slice("Bearer ".length).trim();
}

async function requireAdmin(ctx: any, request: Request) {
  const token = getBearerToken(request);
  if (!token) return false;
  const session = await ctx.runQuery(api.admin.validateSession, { token });
  return session.ok === true;
}

http.route({
  path: "/api/auth/login",
  method: "OPTIONS",
  handler: httpAction(async () => noContent()),
});

http.route({
  path: "/api/auth/login",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const body = await request.json();
    const password = String(body.password ?? "");
    const expectedPassword = process.env.ADMIN_PASSWORD ?? "admin";
    if (!password || password !== expectedPassword) {
      return json({ ok: false, error: "Invalid password" }, 401);
    }

    const token = crypto.randomUUID();
    const created = await ctx.runMutation(api.admin.createSession, { token });
    return json({ ok: true, token, expiresAt: created.expiresAt });
  }),
});

http.route({
  path: "/api/auth/me",
  method: "OPTIONS",
  handler: httpAction(async () => noContent()),
});

http.route({
  path: "/api/auth/me",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const token = getBearerToken(request);
    if (!token) return json({ ok: false }, 401);
    const session = await ctx.runQuery(api.admin.validateSession, { token });
    if (!session.ok) return json({ ok: false }, 401);
    return json({ ok: true, expiresAt: session.expiresAt });
  }),
});

http.route({
  path: "/api/auth/logout",
  method: "OPTIONS",
  handler: httpAction(async () => noContent()),
});

http.route({
  path: "/api/auth/logout",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const token = getBearerToken(request);
    if (!token) return json({ ok: false }, 401);
    await ctx.runMutation(api.admin.revokeSession, { token });
    return json({ ok: true });
  }),
});

http.route({
  path: "/api/guests",
  method: "OPTIONS",
  handler: httpAction(async () => noContent()),
});

http.route({
  path: "/api/guests",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    if (!(await requireAdmin(ctx, request))) {
      return json({ ok: false, error: "Unauthorized" }, 401);
    }
    const rows = await ctx.runQuery(api.guests.list, {});
    return json(rows);
  }),
});

http.route({
  path: "/api/guest",
  method: "OPTIONS",
  handler: httpAction(async () => noContent()),
});

http.route({
  path: "/api/guest",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    if (!(await requireAdmin(ctx, request))) {
      return json({ ok: false, error: "Unauthorized" }, 401);
    }
    const body = await request.json();
    const result = await ctx.runMutation(api.guests.add, {
      first_name: body.first_name,
      last_name: body.last_name,
      guest_type: body.guest_type,
      max_party: Number(body.max_party || 1),
      phone: body.phone || undefined,
      email: body.email || undefined,
      deadline: body.deadline || undefined,
      attendance: body.attendance || "invited",
    });
    return json(result);
  }),
});

http.route({
  path: "/api/guest/delete",
  method: "OPTIONS",
  handler: httpAction(async () => noContent()),
});

http.route({
  path: "/api/guest/delete",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    if (!(await requireAdmin(ctx, request))) {
      return json({ ok: false, error: "Unauthorized" }, 401);
    }

    const body = await request.json();
    const guestId = body.guestId as Id<"guests"> | undefined;
    if (!guestId) {
      return json({ ok: false, error: "guestId is required" }, 400);
    }

    const result = await ctx.runMutation(api.guests.remove, { guestId });
    if (!result.deleted) {
      return json({ ok: false, error: "Guest not found" }, 404);
    }

    return json({ ok: true, ...result });
  }),
});

http.route({
  path: "/api/rsvp",
  method: "OPTIONS",
  handler: httpAction(async () => noContent()),
});

http.route({
  path: "/api/rsvp",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const body = await request.json();

    const guestId = body.guest_id ? (body.guest_id as Id<"guests">) : undefined;

    const rsvpResult = await ctx.runMutation(api.rsvps.submit, {
      guest_id: guestId,
      first_name: body.first_name,
      last_name: body.last_name,
      email: body.email,
      phone: body.phone || undefined,
      attendance: body.attendance,
      guest_type: body.guest_type || undefined,
      party_names: body.party_names || undefined,
      meal_preference: body.meal_preference || undefined,
      dietary_requirements: body.dietary_requirements || undefined,
      song_request: body.song_request || undefined,
      message: body.message || undefined,
      submitted_at: body.submitted_at || new Date().toISOString(),
    });

    const guestResult = await ctx.runMutation(api.guests.updateFromRsvp, {
      guestId,
      first_name: body.first_name,
      last_name: body.last_name,
      email: body.email,
      phone: body.phone || undefined,
      attendance: body.attendance,
      guest_type: body.guest_type || undefined,
      message: body.message || undefined,
      submitted_at: body.submitted_at || new Date().toISOString(),
    });

    return json({ ok: true, rsvp: rsvpResult, guest: guestResult });
  }),
});

export default http;
