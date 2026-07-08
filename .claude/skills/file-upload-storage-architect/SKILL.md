---
name: file-upload-storage-architect
description: Design file/object storage and upload flows for a multi-tenant SaaS — direct-to-storage vs proxied upload, short-lived signed URLs scoped to one object + verb + expiry, tenancy by bucket/path-prefix, size/type/CONTENT validation (magic-byte, not just extension), malware scanning, image/derivative processing off the request path, retention/lifecycle, CDN + cache-control, and storage-cost posture. Produces the upload-flow design, the storage-tenancy + signed-URL contract, the validation/scan pipeline, and the retention plan. Use when adding uploads, attachments, or media, when files must be tenant-isolated, or when uploads are slow, unsafe, or unbounded. Do NOT use for the personal-data lifecycle of file CONTENTS — consent, subject-access, deletion SLAs (pii-lifecycle-designer) — or for auditing existing storage RLS/bucket policies (rls-policy-auditor); this designs the storage + upload architecture and defers those.
---

# File Upload Storage Architect

## Purpose

File uploads are a security and cost surface disguised as a convenience:
proxying every byte through the app server wastes compute and caps file
size, a signed URL scoped too broadly hands a client a key to the whole
bucket, trusting the file extension lets an attacker upload an executable as
a `.png`, and unbounded retention quietly turns storage into the biggest
line on the bill. This skill designs the upload and object-storage
architecture so none of that happens: the upload flow (direct vs proxied),
narrowly-scoped short-lived signed URLs, tenancy by bucket/path prefix,
content validation that inspects bytes rather than names, malware scanning,
derivative processing off the request path, and a retention/lifecycle plan.
The deliverable is the upload-flow design, the storage-tenancy and signed-URL
contract, the validation/scan pipeline, and the retention plan. The personal-
data lifecycle of what the files CONTAIN belongs to `pii-lifecycle-designer`;
this owns the storage architecture.

## Use When

- Use when: adding file uploads, attachments, avatars, document/media
  storage, or import/export of files to/from object storage.
- Use when: files must be tenant-isolated and you need the bucket/path and
  access-control design that guarantees one tenant cannot read another's
  objects.
- Use when: uploads are slow (proxied through the app), unsafe (extension-
  trusted, unscanned), or unbounded (no size cap, no retention), or signed
  URLs are over-scoped or long-lived.
- Use when: choosing direct-to-storage vs proxied upload, or designing
  image/thumbnail/transcode derivative processing.
- Do NOT use when: the concern is the PERSONAL-DATA lifecycle of file
  contents — lawful basis/consent, data-subject access and export, deletion
  SLAs, PII classification of what's inside the file — that is
  `pii-lifecycle-designer`; this skill designs where and how files are
  stored, not the privacy obligations on their contents.
- Do NOT use when: the task is auditing EXISTING storage RLS / bucket
  policies for holes — that is `rls-policy-auditor`; this skill DESIGNS the
  storage access model, and hands policy auditing there.
- Do NOT use when: the "file" is really structured data that belongs in the
  database, not object storage — say so rather than designing storage for it.

## Inputs to Inspect

1. What is uploaded: file types, expected and maximum sizes, volume per
   tenant, and whether files are user-facing (avatars, attachments) or
   pipeline inputs (imports, media to transcode).
2. Who may upload and who may read each object: the authorization model
   (`authorization-matrix-designer`) mapping to object access, and whether
   any objects are public (and must be, deliberately).
3. Current upload path: proxied through the app vs direct to storage, how
   URLs are signed today (scope, expiry), and any incident history (oversized
   uploads, malicious files, cross-tenant access).
4. The tenant model (`multi-tenant-data-architect`): pooled vs siloed, so
   storage tenancy (shared bucket + path prefix vs per-tenant bucket) matches.
5. Storage backend and its features: signed-URL support, object-level access
   control, lifecycle rules, versioning, and CDN integration available.
6. Downstream processing: derivatives needed (thumbnails, transcodes, text
   extraction), and whether scanning/processing must complete before the
   file is usable.

## Workflow

1. **Choose the upload flow.** Direct-to-storage (client uploads straight to
   object storage via a signed URL; the app never touches the bytes) is the
   default for size and cost — it removes the app server from the data path.
   Proxied (through the app) only when the app must inspect/transform every
   byte inline, accepting the size cap and compute cost. State the choice and
   why. For direct uploads, the app issues a signed URL and RECORDS the
   intended object; it does not trust the client to report success.
2. **Scope signed URLs narrowly and briefly.** A signed URL grants exactly
   one verb (PUT for upload, GET for download) on exactly one object key, with
   a short expiry (minutes, not days), and — for uploads — a content-length
   and content-type constraint where the backend supports it. Never issue a
   URL scoped to a prefix or bucket. The object key is server-derived from
   the tenant + a random id, never a client-supplied path.
3. **Design storage tenancy.** Shared bucket with a mandatory tenant path
   prefix (`<tenant-id>/<random-object-id>`) or per-tenant buckets, chosen to
   match the data-tenancy model. The access rule: a signed URL or policy for
   tenant A can only ever name keys under A's prefix; a client cannot craft a
   key that escapes its tenant. Hand the resulting bucket/RLS policy to
   `rls-policy-auditor` for verification.
4. **Validate on CONTENT, not name.** Enforce the size cap at the storage
   layer (not just client-side), and validate type by magic bytes / content
   sniffing, not the extension or the client-sent MIME type. Reject or
   quarantine mismatches. State that a `.png` whose bytes are an executable is
   rejected.
5. **Scan before use.** Route uploaded files through malware/content scanning
   BEFORE they are served or processed; hold them in a quarantine/pending
   state until scanned clean. Define the scan-failure path (delete + alert)
   and the not-yet-scanned state (not downloadable). Do not serve user-uploaded
   files from the app's own origin/domain in a way that enables stored-XSS —
   serve from an isolated domain / with safe content-disposition.
6. **Process derivatives off the request path.** Thumbnails, transcodes, and
   text extraction run as background jobs (compose
   `background-job-orchestration-architect`), not inline in the upload
   request — with the original immutable and derivatives regenerable.
7. **Design retention and lifecycle.** Per object class: retention period,
   lifecycle transitions (hot → cold/archive), orphan cleanup (objects whose
   DB record was deleted), and deletion propagation (deleting the record
   deletes the object). Storage without a retention rule grows forever — name
   the cost. Actual PII deletion SLAs defer to `pii-lifecycle-designer`.
8. **Design serving.** CDN + cache-control for public/cacheable objects;
   signed short-lived GET URLs for private objects (never a public URL for
   private data); and cache-invalidation on replacement. State the private-vs-
   public decision per object class explicitly.
9. **Deliver** the upload-flow design, tenancy + signed-URL contract,
   validation/scan pipeline, and retention plan in the Output Format.

## Output Format

```
FILE UPLOAD & STORAGE DESIGN — <system/domain>
Upload flow:    <direct-to-storage | proxied> + why; app records intent, does
  not trust client success report
Signed URLs:    <one verb + one object key + short expiry + size/type constraint;
  never prefix/bucket-scoped; key = server-derived tenant/<random-id>>
Storage tenancy: <shared bucket + tenant prefix | per-tenant bucket>; a signed
  URL/policy for A names only A's keys → policy audit to rls-policy-auditor
Validation:     <storage-enforced size cap; magic-byte/content-type check, not
  extension; mismatch → reject/quarantine>
Scanning:       <malware/content scan before serve/process; quarantine/pending
  state; scan-fail path; safe serving domain / content-disposition (no stored XSS)>
Derivatives:    <thumbnails/transcodes/extraction as background jobs (→
  background-job-orchestration-architect); original immutable, derivatives regenerable>
Retention:      <per class: retention, lifecycle transitions, orphan cleanup,
  delete-record→delete-object>; PII deletion SLAs → pii-lifecycle-designer
Serving:        <CDN + cache-control for public; signed short-lived GET for
  private; per-class public-vs-private decision>
Cost posture:   <growth per tenant, archive tiering, orphan cost>
Open questions / risks: <each with risk-if-wrong / who answers>
```

## Validation Checklist

- [ ] Upload flow (direct vs proxied) is chosen with a stated reason; direct
      uploads have the app record intent and not trust a client success report.
- [ ] Signed URLs grant one verb on one object key with a short expiry and
      size/type constraints — never prefix- or bucket-scoped.
- [ ] Object keys are server-derived (`tenant/<random-id>`); a client cannot
      craft a key that escapes its tenant prefix.
- [ ] Size cap is enforced at the storage layer; type is validated by content/
      magic bytes, not extension or client MIME.
- [ ] Files are scanned before serve/process and held in quarantine until
      clean; private files are never served via public URLs; serving avoids
      stored-XSS (isolated domain / safe content-disposition).
- [ ] Derivatives run off the request path; the original is immutable.
- [ ] Every object class has retention, orphan cleanup, and delete-propagation;
      unbounded growth is named as cost.
- [ ] Storage access-policy verification is handed to `rls-policy-auditor`;
      PII lifecycle of contents is handed to `pii-lifecycle-designer`.

## Gotchas

- Trusting the file extension or the client-sent MIME type is the malicious-
  upload bug: validate the actual bytes, or a `.png` that is really a script
  or executable sails through.
- A signed URL scoped to a prefix or bucket, or with a multi-day expiry, is a
  bearer key to more than intended — and it can be shared/leaked. One object,
  one verb, minutes of validity.
- A client-supplied object path (`key = req.body.path`) is directory traversal
  into another tenant's data; the key must be server-derived from the tenant.
- Serving user-uploaded HTML/SVG from your app's own domain is stored XSS in
  the making; SVGs carry scripts. Serve from an isolated domain with a safe
  content-disposition, or sanitize.
- Proxying every upload through the app caps file size at the request limit
  and burns app compute on bytes it only forwards — direct-to-storage exists
  for exactly this.
- No retention rule means storage grows forever and orphaned objects (record
  deleted, object left) accumulate silently as cost with no owner.
- "Scanned later" that still serves the file now is "unscanned": the pending
  state must be non-servable, or you serve malware for the scan window.
- A public bucket for "just the avatars" becomes a public bucket for whatever
  gets written there next; default private, make public explicit per class.

## Stop Conditions

- The object-access authorization (who may read/write each object) is
  undefined → obtain it from `authorization-matrix-designer` /
  `multi-tenant-data-architect` before designing signed-URL scope; a signed
  URL enforcing an undefined policy is a false assurance.
- Regulated or highly sensitive file CONTENTS drive real retention/deletion/
  residency obligations → surface them and route the personal-data lifecycle
  to `pii-lifecycle-designer`; this skill designs storage, not the privacy
  obligations on the payload.
- The "file" is structured data better modeled in the database (queried,
  joined, partially updated) → say so; object storage is the wrong home for it.
- Asked to run a bulk migration / lifecycle purge / bucket-policy change
  against live storage → this skill DESIGNS the flow and migration; executing
  destructive storage operations follows the repo's approval path.

## Supporting Files

- `evals/evals.json` — behavior cases: the add-uploads design, the direct-vs-
  proxied + signed-URL-scope edge, the extension-trust rejection, and the PII-
  lifecycle non-trigger.
- `evals/trigger-evals.json` — discrimination against `pii-lifecycle-designer`
  (personal-data lifecycle of contents) and `rls-policy-auditor` (auditing
  existing storage policies).
- No `references/` — the upload/tenancy/validation/retention procedure above
  is complete; detail lives in the produced artifacts.
