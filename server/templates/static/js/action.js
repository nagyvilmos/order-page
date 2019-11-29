export const REQUEST = "REQUEST";
export const REPLY = "REPLY";

export function request(request) {
  return { type: REQUEST, request };
}

export function reply(request, reply) {
  return { type: REPLY, request, reply };
}
