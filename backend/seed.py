"""Seed the database with initial disease data and admin user."""

from backend.extensions import db
from backend.models import User, Disease

SEED_DISEASES = [
    {
        "name": "Tomato - Early Blight",
        "plant": "Tomato",
        "description": "Fungal disease caused by Alternaria solani. Dark brown to black concentric rings on older leaves forming a target-like pattern.",
        "treatment": "1. Remove and destroy infected leaves immediately.\n2. Apply fungicide (chlorothalonil or copper-based) every 7-10 days.\n3. Water at the base of plants to keep foliage dry.\n4. Stake plants to improve air circulation.",
        "prevention": "Rotate crops every 2-3 years. Use disease-resistant varieties. Mulch around plants to prevent soil splash. Space plants adequately for air flow.",
        "chemical_treatment": "Chlorothalonil (Daconil) at first sign of disease. Copper fungicide every 7-14 days preventively. Mancozeb alternated with chlorothalonil for resistance management.",
    },
    {
        "name": "Tomato - Late Blight",
        "plant": "Tomato",
        "description": "Caused by Phytophthora infestans. Large dark water-soaked lesions on leaves and stems. Can destroy entire crops rapidly.",
        "treatment": "1. Remove and destroy ALL infected plant material.\n2. Apply systemic fungicide immediately.\n3. Improve drainage around plants.\n4. In severe cases remove entire plants to prevent spread.",
        "prevention": "Plant resistant varieties. Avoid overhead irrigation. Ensure good air circulation. Monitor weather conditions as cool wet weather favors this disease.",
        "chemical_treatment": "Mefenoxam (Ridomil Gold) for systemic protection. Chlorothalonil as contact fungicide for prevention. Copper hydroxide as organic option applied before symptoms.",
    },
    {
        "name": "Tomato - Leaf Mold",
        "plant": "Tomato",
        "description": "Caused by Passalora fulva. Yellow spots on upper leaf surfaces with olive-green to brown velvety mold underneath.",
        "treatment": "1. Improve ventilation in greenhouses.\n2. Remove infected leaves.\n3. Reduce humidity below 85%.\n4. Apply appropriate fungicide.",
        "prevention": "Use resistant varieties. Maintain good air circulation. Avoid wetting leaves when watering. Keep humidity below 85%.",
        "chemical_treatment": "Chlorothalonil preventively. Copper-based fungicides for organic production. Mancozeb as effective contact fungicide.",
    },
    {
        "name": "Potato - Early Blight",
        "plant": "Potato",
        "description": "Caused by Alternaria solani. Brown-black lesions with concentric rings on older leaves. Can cause significant yield loss.",
        "treatment": "1. Remove infected foliage.\n2. Apply fungicide on 7-day schedule during wet weather.\n3. Harvest tubers when skin is set.\n4. Avoid injuring tubers during harvest.",
        "prevention": "Use certified disease-free seed potatoes. Practice 3-year crop rotation. Maintain adequate soil fertility. Destroy volunteer potato plants.",
        "chemical_treatment": "Azoxystrobin (Quadris) preventively. Chlorothalonil every 7-10 days. Mancozeb as protectant fungicide.",
    },
    {
        "name": "Potato - Late Blight",
        "plant": "Potato",
        "description": "Caused by Phytophthora infestans. Water-soaked lesions that rapidly turn brown and necrotic. The same pathogen that caused the Irish Potato Famine.",
        "treatment": "1. Destroy all infected plant material.\n2. Apply systemic fungicide immediately.\n3. Hill soil around plants to protect tubers.\n4. Harvest only in dry conditions.",
        "prevention": "Plant certified disease-free seed. Eliminate cull piles and volunteer plants. Monitor forecasts for blight-favorable weather. Use resistant varieties.",
        "chemical_treatment": "Mefenoxam + Chlorothalonil for active infections. Fluopicolide (Presidio) for systemic protection. Cymoxanil + Famoxadone for curative and preventive use.",
    },
    {
        "name": "Apple - Apple Scab",
        "plant": "Apple",
        "description": "Caused by Venturia inaequalis. Olive-green to dark brown lesions on leaves and fruit. Severely infected leaves may curl and drop.",
        "treatment": "1. Rake and destroy fallen leaves in autumn.\n2. Prune trees to improve air circulation.\n3. Apply fungicide from bud break through petal fall.\n4. Remove severely infected fruit.",
        "prevention": "Plant scab-resistant varieties such as Liberty or Enterprise. Remove fallen leaves and fruit. Prune for open canopy. Apply dormant sprays.",
        "chemical_treatment": "Captan as standard protectant spray. Myclobutanil (Rally) as systemic fungicide. Sulfur as organic option applied before rain events.",
    },
    {
        "name": "Corn - Common Rust",
        "plant": "Corn",
        "description": "Caused by Puccinia sorghi. Small round to elongated brown pustules on both leaf surfaces releasing powdery rust-colored spores.",
        "treatment": "1. Apply foliar fungicide if infection detected early.\n2. Monitor fields regularly during humid conditions.\n3. Remove heavily infected plants in small gardens.",
        "prevention": "Plant resistant hybrids. Early planting to avoid peak spore periods. Maintain balanced fertilization. Scout fields regularly.",
        "chemical_treatment": "Azoxystrobin + Propiconazole for broad spectrum control. Pyraclostrobin (Headline) for systemic activity. Trifloxystrobin (Flint) for preventive application.",
    },
    {
        "name": "Grape - Black Rot",
        "plant": "Grape",
        "description": "Caused by Guignardia bidwellii. Circular tan lesions with dark borders on leaves. Fruit shrivels into hard black mummies.",
        "treatment": "1. Remove and destroy mummified fruit and infected canes.\n2. Apply fungicide from bud break to veraison.\n3. Improve canopy management for air flow.\n4. Remove wild grapes nearby.",
        "prevention": "Sanitation is critical: remove all mummies. Open canopy for air and sunlight. Maintain regular spray program. Remove wild grapes within 100 feet.",
        "chemical_treatment": "Myclobutanil (Rally) at key growth stages. Mancozeb as early season protectant. Captan as good protectant option.",
    },
    {
        "name": "Healthy Plant",
        "plant": "Various",
        "description": "No disease detected. The plant appears healthy with no visible signs of infection, discoloration, or damage.",
        "treatment": "No treatment needed. Continue regular plant care and monitoring.",
        "prevention": "Maintain proper watering schedule. Ensure adequate nutrition. Monitor regularly for early signs of disease. Practice good garden hygiene.",
        "chemical_treatment": "No chemical treatment required. Preventive neem oil applications can help maintain plant health.",
    },
]


def seed_database():
    if Disease.query.count() == 0:
        for data in SEED_DISEASES:
            db.session.add(Disease(**data))
        db.session.commit()

    if not User.query.filter_by(is_admin=True).first():
        admin = User(name="Admin", email="admin@plantdoc.com", is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
