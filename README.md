# POS UI — Web + Mobile

A shared UI foundation for the Personal Operating System.

## Architecture

```text
packages/shared
       ├───────────────┐
       ↓               ↓
     web             mobile
   React/Vite       Expo/RN
       │               │
       └──────→ POS backend
                 /kundli/calculate
```

The web and mobile clients share types, constants and the API client, while
their presentation code stays platform-native.

## 1. Backend

Run the existing POS backend first:

```bash
cd ../pos_backend
pip install -r requirements.txt
uvicorn app:app --reload
```

## 2. Install UI dependencies

From this folder:

```bash
npm install
```

## 3. Web

```bash
npm run web
```

Set a different API URL with:

```bash
VITE_API_BASE=http://YOUR_BACKEND:8000 npm run web
```

Build:

```bash
npm run web:build
```

## 4. Mobile

```bash
npm run mobile
```

For a physical device, set:

```bash
EXPO_PUBLIC_API_BASE=http://YOUR_COMPUTER_LAN_IP:8000
```

The mobile client is intentionally a native Expo/React Native app rather
than a wrapped website. This gives us a clean route to App Store / Play Store
while keeping the web product independently deployable.

## Current product scope

- Birth details entry
- D1 chart result
- Ascendant
- Planetary placements
- Vargas view
- Bhava-ready UI boundary
- POS trait architecture visualization
- Shared API contract
- Responsive web UI
- Native mobile UI

The displayed trait values in the first UI pass are visual placeholders until
the POS endpoint returns actual computed trait values. They are not presented
as calculated user data.
