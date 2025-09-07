from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import pandas as pd
import json
import os
from datetime import datetime, timedelta

# 📁 Initialisation
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI()

# 🔧 Configuration des répertoires statiques et templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

# 📊 Import de la fonction de visualisation
try:
    from visualisation import generate_graphs
    print("✅ Module visualisation.py importé avec succès")
except ImportError as e:
    print(f"❌ Erreur d'import de visualisation.py : {e}")

# 🏠 Page d'accueil
@app.get("/", response_class=HTMLResponse)
def accueil():
    return "<h1>Bienvenue 👋</h1><a href='/dashboard'>Voir le dashboard</a>"

# 📊 Dashboard de visualisation
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    try:
        graph1, graph2 = generate_graphs()
        return templates.TemplateResponse("st.html", {
            "request": request,
            "graph1": graph1,
            "graph2": graph2
        })
    except Exception as e:
        print(f"Erreur dans la route dashboard : {e}")
        return HTMLResponse(
            content=f"<h1>Erreur</h1><p>Impossible de générer les graphiques: {str(e)}</p>",
            status_code=500
        )

# 📦 Modèles Pydantic pour les prédictions
class PredictionInput(BaseModel):
    year: int
    month: int
    product_encoded: int
    boxes_shipped: int

class BestSellerPrediction(BaseModel):
    months_ahead: int
    current_season: str  # summer, winter, spring, autumn

# 🔁 Charger le mapping des labels produits
def load_label_mapping():
    label_path = os.path.join(BASE_DIR, "modele", "modele", "label_mapping.json")
    with open(label_path, "r", encoding="utf-8") as f:
        return {int(k): v for k, v in json.load(f).items()}

# 🎯 Prédiction simple
@app.post("/predict")
def predict(input: PredictionInput):
    try:
        model_path = os.path.join(BASE_DIR, "modele", "modele", "model_regression.pkl")
        model = joblib.load(model_path)

        label_mapping_path = os.path.join(BASE_DIR, "modele", "modele", "label_mapping.json")
        with open(label_mapping_path, "r", encoding="utf-8") as f:
            label_mapping = json.load(f)

        X = pd.DataFrame([{
        "product_encoded": input.product_encoded,
        "boxes_shipped": input.boxes_shipped,
        "month": input.month,
        "year": input.year}])

        prediction = model.predict(X)[0]

        product_name = label_mapping.get(str(input.product_encoded), "Produit inconnu")
        return {
            "product_name": product_name  # 👉 Retourne uniquement le nom du produit
        }
    except Exception as e:
        print("⚠️ ERREUR dans la route /predict :", e)
        return JSONResponse(
            content={"prediction": "Erreur lors de la prédiction", "message": str(e)},
            status_code=500
        )



@app.post("/predict-bestseller")
def predict_bestseller(input: BestSellerPrediction):
    try:
        model = joblib.load(os.path.join(BASE_DIR, "modele", "modele", "model_regression.pkl"))
        label_mapping = load_label_mapping()
        df = pd.read_csv(os.path.join(BASE_DIR, "modele", "modele", "chocolate_sales.csv"))

        future_date = datetime.now() + timedelta(days=30 * input.months_ahead)

        chocolate_types = {
            "Chocolat Noir": {"seasonal_boost": {"winter": 1.3, "summer": 0.9}},
            "Chocolat au Lait": {"seasonal_boost": {"winter": 1.1, "summer": 1.2}},
            "Chocolat Blanc": {"seasonal_boost": {"winter": 1.0, "summer": 1.4}},
            "Chocolat aux Noisettes": {"seasonal_boost": {"winter": 1.2, "summer": 1.0}},
            "Chocolat aux Amandes": {"seasonal_boost": {"winter": 1.1, "summer": 1.1}}
        }

        predictions = []
        for chocolate_name, data in chocolate_types.items():
            seasonal_multiplier = data["seasonal_boost"].get(input.current_season, 1.0)

            avg_boxes = df[df["product"] == chocolate_name]["boxes_shipped"].mean() or 100
            avg_dh = df[df["product"] == chocolate_name]["amount_in_dh"].mean() or 1000

            adjusted_boxes = int(avg_boxes * seasonal_multiplier)
            adjusted_dh = int(avg_dh * seasonal_multiplier)

            X = [[0, adjusted_boxes, future_date.month, future_date.year]]
            prediction = model.predict(X)[0]

            predicted_label = round(prediction)
            predicted_product = label_mapping.get(predicted_label, "Produit inconnu")

            predictions.append({
                "product": predicted_product,
                "based_on": chocolate_name,
                "predicted_score": float(prediction),
                "estimated_boxes": adjusted_boxes,
                "seasonal_factor": seasonal_multiplier,
                "prediction_date": future_date.strftime("%Y-%m-%d")
            })

        predictions.sort(key=lambda x: x["predicted_score"], reverse=True)
        best_seller = predictions[0]

        recommendations = []
        if best_seller["seasonal_factor"] > 1.1:
            recommendations.append(f"📈 Boost saisonnier: x{best_seller['seasonal_factor']:.1f}")
        recommendations.append(
            "⚡ Prédiction à court terme - plus fiable" if input.months_ahead <= 2
            else "🔮 Prédiction à long terme - incertitude plus élevée"
        )

        return {
            "status": "success",
            "prediction_period": f"{input.months_ahead} mois dans le futur",
            "target_date": future_date.strftime("%B %Y"),
            "best_seller": best_seller,
            "top_3_predictions": predictions[:3],
            "all_predictions": predictions,
            "recommendations": recommendations,
            "season_analyzed": input.current_season
        }

    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": f"Erreur de prédiction: {str(e)}"},
            status_code=500
        )


@app.post("/predict-simple")
def predict_simple():
    try:
        input_data = BestSellerPrediction(months_ahead=3, current_season="summer")
        result = predict_bestseller(input_data)

        if result.get("status") == "success":
            best = result["best_seller"]
            return {
                "prediction": f"🏆 Meilleur chocolat prédit: {best['product']} avec un score de {best['predicted_score']:.2f}",
                "details": f"Estimation: {best['estimated_boxes']} boîtes en {result['target_date']}",
                "status": "success"
            }
        return result
    except Exception as e:
        return {"prediction": f"Erreur de prédiction: {str(e)}", "status": "error"}


# 🔄 Regénérer les graphiques
@app.get("/regenerate-graphs")
def regenerate_graphs():
    try:
        graph1, graph2 = generate_graphs()
        return {"status": "success", "message": "Graphiques régénérés avec succès"}
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": f"Erreur: {str(e)}"},
            status_code=500
        )

# 🧾 Afficher le formulaire de vente
@app.get("/sells", response_class=HTMLResponse)
async def show_sells_form(request: Request):
    return templates.TemplateResponse("sells.html", {"request": request})

# ➕ Enregistrer une nouvelle vente
class Sell(BaseModel):
    client_name: str
    product: str
    date: str
    amount_in_dh: float
    boxes_shipped: int

@app.post("/add-sell")
async def add_sell(sell: Sell):
    try:
        csv_file = os.path.join(BASE_DIR, "modele", "chocolate_sales.csv")
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
        else:
            df = pd.DataFrame(columns=["client_name", "product", "date", "amount_in_dh", "boxes_shipped"])
        new_row = pd.DataFrame([sell.dict()])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(csv_file, index=False)
        return {"success": True}
    except Exception as e:
        return {"success": False, "message": str(e)}

# 🔎 Récupérer les données du dashboard
@app.get("/dashboard-data")
def get_dashboard_data():
    try:
        graph1, graph2 = generate_graphs()
        return {"status": "success", "graph1": graph1, "graph2": graph2}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

# 🚀 Exécution locale
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
