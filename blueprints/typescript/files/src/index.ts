/** Return a deterministic greeting for the supplied name. */
export function greet(name: string): string {
  const normalized = name.trim();
  if (normalized.length === 0) {
    throw new TypeError("name must not be empty");
  }
  return `Hello, ${normalized}!`;
}
