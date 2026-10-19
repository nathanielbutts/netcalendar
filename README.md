# Net Tracking Calendar

A static, client-side net schedule for GitHub Pages. No build tools, backend, or dependencies.

## Deployment

1. Create or use the GitHub repository `nathanielbutts/netcalendar`.
2. Upload `index.html` and `nets.json` to the root of the repository.
3. In **Settings → Pages**, set the publishing source to **Deploy from a branch**, `main`, `/ (root)` (or use your existing Pages workflow).
4. Open https://nathanielbutts.github.io/netcalendar/ after deployment.

## Editing

You can edit `nets.json` in any text editor or use the site's **Add net** / **Manage nets** interface. Browser edits are stored in localStorage on that device; they do **not** modify the GitHub repository. Click **Download nets.json**, then upload and commit the replacement on GitHub to publish updates. Visitors see published data unless they have saved a browser override.

## JSON format

```json
{
  "version": 1,
  "nets": [
    {
      "id": "unique-name",
      "name": "Example Net",
      "frequency": "147.330 MHz / PL 100.0 Hz",
      "mode": "FM",
      "notes": "Winlink: example@winlink.org",
      "startUtc": "23:00",
      "durationMinutes": 60,
      "recurrence": { "type": "weekdays", "days": [0, 3, 6] },
      "enabled": true
    }
  ]
}
```

- Weekday numbers are **UTC**: 0 Sunday, 1 Monday, ... 6 Saturday.
- Daily: `{ "type": "daily" }`.
- Selected weekdays: `{ "type": "weekdays", "days": [1, 3, 5] }`.
- Monthly nth weekday: `{ "type": "monthly", "ordinal": 2, "weekday": 4 }` (second Thursday).
- Last weekday of month: `{ "type": "monthly", "ordinal": -1, "weekday": 5 }`.
- Fifth weekday: `ordinal: 5` (only months with a fifth occurrence).
- Each record's `startUtc` is a fixed UTC clock time. The web editor can accept local times and convert them into UTC using the local offset on the currently selected date. If you need a net to always run at the same *local time* across daylight-saving changes, it needs a time-zone-aware recurrence rather than a fixed UTC time.
- Maximum individual duration: 1440 minutes (24 hours).

## Time displays and alerts

The timeline shows 30 continuous hours beginning with the earliest currently running net (or the current UTC hour if none is running) in Live view. The red vertical line is the live UTC time whenever within the viewed interval. Left column is sticky during horizontal scrolling. UTC dates are written alongside the hour ticks for transitions across midnight. Live/Now resets the timeline. Previous/Next browse UTC calendar dates.

The **15-minute alerts** option displays a notification within the page when a net approaches. The page must remain open; this is not a desktop push notification or a background notification service.

The example nets are fictional placeholders, not verified on-air nets.
