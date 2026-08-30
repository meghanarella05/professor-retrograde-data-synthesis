<<<<<<< HEAD
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
=======
# POS Backend — v0.1

Backend prototype for the Personal Operating System (POS) model.

## Architecture

`birth details -> Kundli engine -> canonical chart JSON -> POS engine -> structured output -> narrative/app layer`

This repository currently implements the **POS interpretation layer**. The Kundli/astronomical calculation layer is deliberately kept separate so it can be swapped in later.

## Model

The supplied specification defines a 20-dimensional latent trait vector:

`O, C, E, A, ES, Cur, AD, D, Cr, Ad, ER, R, As, Em, Att, RT, Au, P, ST, SC`

Each operator is component-wise:

`f_X(T) = (w1*T1, ..., w20*T20)`

No traits are summed or collapsed by the operator layer.

The coefficient tables in `pos_engine/config.json` are transcribed from the supplied POS specification. The model is versioned as `pos-v1`.

## Run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
>>>>>>> 33aa07e4a50b0983a6c153546e8c75149d07e493
pip install -r requirements.txt
uvicorn app:app --reload
```

<<<<<<< HEAD
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
=======
Open API docs at `http://127.0.0.1:8000/docs`.

## Example

```bash
curl http://127.0.0.1:8000/health
```

Then POST `/interpret` with a chart and 20 base traits.

## Important boundary

This is a software implementation of the supplied model. It does not establish that astrological chart features scientifically determine personality. The backend should expose model outputs as model-derived interpretations rather than clinical or factual psychological diagnoses.

## Kundli module

`kundli_engine/` now provides an MVP chart-calculation boundary using Swiss Ephemeris:

- Lahiri sidereal mode
- planetary longitudes
- Ascendant
- whole-sign houses
- Rahu/Ketu
- retrograde flags
- canonical JSON suitable for the POS layer

The current divisional-chart fields are a boundary for the next implementation pass. Do not mix astronomical calculation code into `pos_engine/`.

## API

```text
GET  /health
GET  /model
POST /kundli/calculate
POST /interpret
```

The Swagger UI is available at `/docs` when the server is running.

## Example flow

1. `POST /kundli/calculate` with birth details.
2. Persist/cache the returned canonical chart.
3. Feed the chart into `/interpret` together with the base 20-dimensional trait vector.
4. Keep narrative/LLM generation as a separate layer from deterministic model computation.

>>>>>>> 33aa07e4a50b0983a6c153546e8c75149d07e493
