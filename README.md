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
pip install -r requirements.txt
uvicorn app:app --reload
```

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

