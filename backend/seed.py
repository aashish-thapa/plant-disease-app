"""Populates diseases table and creates the admin account on first run."""

from backend.extensions import db
from backend.models import User, Disease

SEED_DISEASES = [
    {
        "name": "Tomato - Early Blight",
        "plant": "Tomato",
        "description": "Dark brown to black concentric rings show up on older leaves in a target-like pattern. Caused by the fungus Alternaria solani.",
        "treatment": "1. Remove and destroy infected leaves immediately.\n2. Apply fungicide (chlorothalonil or copper-based) every 7-10 days.\n3. Water at the base of plants to keep foliage dry.\n4. Stake plants to improve air circulation.",
        "prevention": "Rotate crops every 2-3 years. Use disease-resistant varieties. Mulch around plants to prevent soil splash. Space plants adequately for air flow.",
        "chemical_treatment": "Chlorothalonil (Daconil) at first sign of disease. Copper fungicide every 7-14 days preventively. Mancozeb alternated with chlorothalonil for resistance management.",
    },
    {
        "name": "Tomato - Late Blight",
        "plant": "Tomato",
        "description": "Large dark water-soaked lesions on leaves and stems, spreads fast. Same organism (Phytophthora infestans) that caused the Irish Potato Famine.",
        "treatment": "1. Remove and destroy ALL infected plant material.\n2. Apply systemic fungicide immediately.\n3. Improve drainage around plants.\n4. In severe cases remove entire plants to prevent spread.",
        "prevention": "Plant resistant varieties. Avoid overhead irrigation. Ensure good air circulation. Monitor weather conditions as cool wet weather favors this disease.",
        "chemical_treatment": "Mefenoxam (Ridomil Gold) for systemic protection. Chlorothalonil as contact fungicide for prevention. Copper hydroxide as organic option applied before symptoms.",
    },
    {
        "name": "Tomato - Leaf Mold",
        "plant": "Tomato",
        "description": "Yellow spots appear on upper leaf surfaces with olive-green velvety mold growing underneath. Usually a greenhouse problem (Passalora fulva).",
        "treatment": "1. Improve ventilation in greenhouses.\n2. Remove infected leaves.\n3. Reduce humidity below 85%.\n4. Apply appropriate fungicide.",
        "prevention": "Use resistant varieties. Maintain good air circulation. Avoid wetting leaves when watering. Keep humidity below 85%.",
        "chemical_treatment": "Chlorothalonil preventively. Copper-based fungicides for organic production. Mancozeb as effective contact fungicide.",
    },
    {
        "name": "Potato - Early Blight",
        "plant": "Potato",
        "description": "Brown-black lesions with concentric rings on older leaves, similar to tomato early blight (same pathogen, Alternaria solani). Can cut yields a lot if untreated.",
        "treatment": "1. Remove infected foliage.\n2. Apply fungicide on 7-day schedule during wet weather.\n3. Harvest tubers when skin is set.\n4. Avoid injuring tubers during harvest.",
        "prevention": "Use certified disease-free seed potatoes. Practice 3-year crop rotation. Maintain adequate soil fertility. Destroy volunteer potato plants.",
        "chemical_treatment": "Azoxystrobin (Quadris) preventively. Chlorothalonil every 7-10 days. Mancozeb as protectant fungicide.",
    },
    {
        "name": "Potato - Late Blight",
        "plant": "Potato",
        "description": "Water-soaked lesions that rapidly turn brown and necrotic. Phytophthora infestans, same thing that caused the Irish Potato Famine.",
        "treatment": "1. Destroy all infected plant material.\n2. Apply systemic fungicide immediately.\n3. Hill soil around plants to protect tubers.\n4. Harvest only in dry conditions.",
        "prevention": "Plant certified disease-free seed. Eliminate cull piles and volunteer plants. Monitor forecasts for blight-favorable weather. Use resistant varieties.",
        "chemical_treatment": "Mefenoxam + Chlorothalonil for active infections. Fluopicolide (Presidio) for systemic protection. Cymoxanil + Famoxadone for curative and preventive use.",
    },
    {
        "name": "Apple - Apple Scab",
        "plant": "Apple",
        "description": "Olive-green to dark brown lesions on leaves and fruit from Venturia inaequalis. Bad infections make leaves curl up and fall off.",
        "treatment": "1. Rake and destroy fallen leaves in autumn.\n2. Prune trees to improve air circulation.\n3. Apply fungicide from bud break through petal fall.\n4. Remove severely infected fruit.",
        "prevention": "Plant scab-resistant varieties such as Liberty or Enterprise. Remove fallen leaves and fruit. Prune for open canopy. Apply dormant sprays.",
        "chemical_treatment": "Captan as standard protectant spray. Myclobutanil (Rally) as systemic fungicide. Sulfur as organic option applied before rain events.",
    },
    {
        "name": "Corn - Common Rust",
        "plant": "Corn",
        "description": "Small brownish pustules on both sides of leaves that release powdery rust-colored spores. The fungus is Puccinia sorghi.",
        "treatment": "1. Apply foliar fungicide if infection detected early.\n2. Monitor fields regularly during humid conditions.\n3. Remove heavily infected plants in small gardens.",
        "prevention": "Plant resistant hybrids. Early planting to avoid peak spore periods. Maintain balanced fertilization. Scout fields regularly.",
        "chemical_treatment": "Azoxystrobin + Propiconazole for broad spectrum control. Pyraclostrobin (Headline) for systemic activity. Trifloxystrobin (Flint) for preventive application.",
    },
    {
        "name": "Grape - Black Rot",
        "plant": "Grape",
        "description": "Circular tan spots with dark borders on leaves. Infected fruit shrivels into hard black mummies. Guignardia bidwellii.",
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
    {
        "name": "Apple - Black Rot",
        "plant": "Apple",
        "description": "Brown rotting lesions on fruit and frogeye leaf spots. You'll also see cankers forming on branches. Botryosphaeria obtusa.",
        "treatment": "1. Prune out dead or infected branches during dormant season.\n2. Remove mummified fruit from trees and ground.\n3. Apply fungicide at bud break.\n4. Maintain tree vigor through proper fertilization.",
        "prevention": "Keep orchard clean of fallen debris. Prune regularly. Remove wild or abandoned apple trees nearby. Good air circulation helps.",
        "chemical_treatment": "Captan applied from green tip through second cover spray. Thiophanate-methyl for canker infections. Myclobutanil as systemic option.",
    },
    {
        "name": "Apple - Cedar Apple Rust",
        "plant": "Apple",
        "description": "Bright yellow-orange spots show up on apple leaves, sometimes with tiny black dots in the center. Needs juniper or cedar trees nearby to complete its life cycle.",
        "treatment": "1. Remove nearby juniper or red cedar trees if possible.\n2. Apply fungicide starting at pink bud stage.\n3. Remove heavily infected leaves.\n4. Plant resistant apple varieties.",
        "prevention": "Separate apple and cedar/juniper plantings by at least a few hundred feet. Choose resistant cultivars like Liberty or Freedom. Scout for galls on junipers.",
        "chemical_treatment": "Myclobutanil from pink through petal fall. Triadimefon as alternative. Fenarimol applied preventively.",
    },
    {
        "name": "Cherry - Powdery Mildew",
        "plant": "Cherry",
        "description": "White powdery coating that shows up on leaves and shoots, sometimes fruit too. Leaves curl and get distorted. Podosphaera clandestina.",
        "treatment": "1. Remove infected shoots during pruning.\n2. Apply fungicide at first sign of white patches.\n3. Improve air flow by thinning canopy.\n4. Water at soil level to keep foliage dry.",
        "prevention": "Avoid excessive nitrogen fertilization. Prune for open canopy. Plant in well-drained areas with good sun exposure.",
        "chemical_treatment": "Sulfur sprays early in infection. Myclobutanil for systemic control. Potassium bicarbonate as organic option.",
    },
    {
        "name": "Corn - Cercospora Leaf Spot",
        "plant": "Corn",
        "description": "Rectangular gray-tan lesions running parallel to the leaf veins. Shows up a lot in humid weather. Also called gray leaf spot (Cercospora zeae-maydis).",
        "treatment": "1. Apply foliar fungicide if detected before tasseling.\n2. Improve field drainage.\n3. Scout regularly during humid weather.\n4. Consider earlier harvest if severe.",
        "prevention": "Rotate away from corn for 1-2 years. Tillage to bury infected residue. Plant resistant hybrids. Avoid planting corn after corn.",
        "chemical_treatment": "Pyraclostrobin + Metconazole at VT/R1 growth stage. Azoxystrobin as preventive. Propiconazole for moderate pressure.",
    },
    {
        "name": "Corn - Northern Leaf Blight",
        "plant": "Corn",
        "description": "Long cigar-shaped gray-green lesions, can be 1 to 6 inches. Gets bad during wet seasons and can really hurt yields. Exserohilum turcicum.",
        "treatment": "1. Apply fungicide before or at tassel if lesions found on upper leaves.\n2. Remove volunteer corn plants.\n3. Monitor regularly during wet seasons.",
        "prevention": "Plant resistant hybrids. Rotate crops away from corn. Tillage helps break down residue. Balance nitrogen fertilization.",
        "chemical_treatment": "Azoxystrobin + Propiconazole at tasseling. Picoxystrobin for extended protection. Trifloxystrobin as protectant.",
    },
    {
        "name": "Grape - Esca Black Measles",
        "plant": "Grape",
        "description": "Multiple fungi involved, not just one. Leaves get a tiger-stripe pattern, berries develop dark spots. Often kills the whole vine eventually.",
        "treatment": "1. Remove and burn severely infected vines.\n2. Protect pruning wounds with wound sealant.\n3. Retrain suckers from below graft union if trunk is compromised.\n4. Reduce vine stress.",
        "prevention": "Make pruning cuts during dry weather. Avoid large pruning wounds. Keep vines vigorous but not over-watered. No reliable chemical control exists.",
        "chemical_treatment": "No consistently effective chemical treatment. Some growers try thiophanate-methyl on pruning wounds. Sodium arsenite was used historically but is now banned.",
    },
    {
        "name": "Grape - Leaf Blight",
        "plant": "Grape",
        "description": "Angular brown spots on leaves with a yellow halo around them. Mostly shows up on the lower leaves first. Also called Isariopsis leaf spot.",
        "treatment": "1. Remove infected leaves from the vine and ground.\n2. Improve canopy airflow with shoot thinning.\n3. Apply protectant fungicide if recurring.\n4. Harvest grapes before significant defoliation.",
        "prevention": "Canopy management is key. Leaf pull in the fruiting zone. Avoid overhead irrigation. Remove basal leaves to improve air movement.",
        "chemical_treatment": "Mancozeb as protectant early season. Copper-based sprays for organic vineyards. Myclobutanil if pressure is high.",
    },
    {
        "name": "Orange - Huanglongbing",
        "plant": "Orange",
        "description": "Also called citrus greening. Bacteria spread by a tiny insect (Asian citrus psyllid). Fruit comes out lopsided and bitter, leaves get mottled. No cure exists.",
        "treatment": "1. There is no cure for infected trees.\n2. Remove and destroy infected trees to prevent spread.\n3. Control psyllid populations aggressively.\n4. Replant with disease-free nursery stock.",
        "prevention": "Use certified disease-free nursery trees only. Regular psyllid monitoring and control. Inspect new plantings frequently. Report suspected cases to agricultural authorities.",
        "chemical_treatment": "No chemical cures the tree. Psyllid control: imidacloprid soil drench, dimethoate foliar spray, spinosad for organic. Nutritional sprays may extend tree life but won't cure it.",
    },
    {
        "name": "Peach - Bacterial Spot",
        "plant": "Peach",
        "description": "Small dark water-soaked spots on leaves that fall out and leave shot-holes behind. Fruit gets sunken cracked brown spots. Bacterial, not fungal (Xanthomonas).",
        "treatment": "1. Prune to improve air circulation.\n2. Apply copper sprays at leaf fall.\n3. Avoid overhead irrigation.\n4. Remove severely infected branches.",
        "prevention": "Plant resistant varieties when possible. Site trees in well-drained locations with good air movement. Avoid working among wet trees.",
        "chemical_treatment": "Copper hydroxide at leaf fall and pre-bloom. Oxytetracycline during bloom in severe cases. Myclobutanil is NOT effective (this is bacterial not fungal).",
    },
    {
        "name": "Pepper Bell - Bacterial Spot",
        "plant": "Pepper",
        "description": "Dark water-soaked spots on both leaves and fruit. Leaves turn yellow and drop off. Xanthomonas bacteria, spreads fast when its wet out.",
        "treatment": "1. Remove and destroy infected plants at end of season.\n2. Apply copper-based bactericide early.\n3. Avoid working with plants when wet.\n4. Use drip irrigation instead of overhead.",
        "prevention": "Use certified disease-free seed and transplants. Rotate away from peppers and tomatoes for 2-3 years. Sanitize tools between plants. Avoid excessive nitrogen.",
        "chemical_treatment": "Copper hydroxide + mancozeb tank mix. Acibenzolar-S-methyl (Actigard) for induced resistance. Streptomycin in severe outbreaks (check local regulations).",
    },
    {
        "name": "Squash - Powdery Mildew",
        "plant": "Squash",
        "description": "White powdery patches on the tops of leaves that spread until the whole leaf is covered. Worse in warm dry weather, weirdly enough (most diseases like it wet).",
        "treatment": "1. Remove heavily infected leaves.\n2. Apply fungicide at first signs of white patches.\n3. Keep plants well-watered at soil level.\n4. Improve air flow between plants.",
        "prevention": "Plant resistant varieties. Space plants generously. Avoid late evening watering. Plant in full sun locations.",
        "chemical_treatment": "Potassium bicarbonate for organic. Myclobutanil or triadimefon for conventional. Sulfur as preventive in cool conditions (can burn leaves in heat).",
    },
    {
        "name": "Strawberry - Leaf Scorch",
        "plant": "Strawberry",
        "description": "Irregular purplish blotches on leaves that merge together and make the plant look scorched. Weakens the plant over time if you dont deal with it.",
        "treatment": "1. Mow or remove old foliage after harvest.\n2. Apply fungicide in spring during leaf expansion.\n3. Improve bed drainage.\n4. Thin plants to reduce humidity.",
        "prevention": "Use resistant cultivars. Renovate beds annually by mowing. Avoid overhead watering. Ensure good plant spacing for airflow.",
        "chemical_treatment": "Captan during bloom through harvest. Myclobutanil pre-bloom. Copper sprays in fall after renovation.",
    },
    {
        "name": "Tomato - Bacterial Spot",
        "plant": "Tomato",
        "description": "Small dark raised spots on leaves and fruit with yellow halos. Bacterial (Xanthomonas), so fungicides wont work on this one.",
        "treatment": "1. Remove infected leaves promptly.\n2. Apply copper-based bactericide.\n3. Switch to drip irrigation.\n4. Stake plants to keep foliage off ground.",
        "prevention": "Use disease-free seed and transplants. Rotate out of nightshades for 2-3 years. Don't handle plants when wet. Remove all plant debris at season end.",
        "chemical_treatment": "Copper hydroxide + mancozeb combination. Streptomycin on transplants before field setting. Actigard for systemic resistance induction.",
    },
    {
        "name": "Tomato - Septoria Leaf Spot",
        "plant": "Tomato",
        "description": "Small circular spots with dark borders and gray centers, look closely and you can see tiny black dots. Starts on the bottom leaves and moves up.",
        "treatment": "1. Remove infected lower leaves immediately.\n2. Mulch around plants to stop soil splash.\n3. Apply fungicide on 7-10 day schedule.\n4. Stake or cage plants for better airflow.",
        "prevention": "Rotate crops for 3 years minimum. Remove all plant debris. Avoid overhead watering. Give plants plenty of spacing.",
        "chemical_treatment": "Chlorothalonil every 7-10 days in wet weather. Mancozeb as alternative. Copper-based for organic growers.",
    },
    {
        "name": "Tomato - Spider Mites",
        "plant": "Tomato",
        "description": "Two-spotted spider mite (Tetranychus urticae). Tiny mites cause stippling on leaves, fine webbing on undersides. Thrives in hot dry weather.",
        "treatment": "1. Spray undersides of leaves with strong water jet.\n2. Apply miticide if population is high.\n3. Release predatory mites (Phytoseiulus persimilis) as biocontrol.\n4. Remove heavily infested leaves.",
        "prevention": "Keep plants well-watered (drought stress worsens mites). Avoid broad-spectrum insecticides that kill natural predators. Monitor undersides of leaves weekly.",
        "chemical_treatment": "Abamectin for quick knockdown. Bifenazate (Acramite) as selective miticide. Horticultural oil or insecticidal soap for organic. Rotate chemistries to prevent resistance.",
    },
    {
        "name": "Tomato - Target Spot",
        "plant": "Tomato",
        "description": "Brown spots with concentric rings on leaves, stems, and fruit. Looks similar to early blight but its a different fungus (Corynespora cassiicola). Gets bad in warm humid weather.",
        "treatment": "1. Remove and destroy infected plant material.\n2. Apply fungicide at first symptoms.\n3. Improve airflow around plants.\n4. Reduce leaf wetness by watering at base.",
        "prevention": "Use resistant varieties if available. Rotate crops. Avoid planting tomatoes in same spot year after year. Mulch to reduce splash.",
        "chemical_treatment": "Chlorothalonil as contact protectant. Azoxystrobin for systemic activity. Difenoconazole for curative action.",
    },
    {
        "name": "Tomato - Yellow Leaf Curl Virus",
        "plant": "Tomato",
        "description": "Viral, spread by whiteflies. Leaves curl upward and turn yellow, plant gets stunted and stops making fruit. Once a plant has it theres no fixing it.",
        "treatment": "1. Remove and destroy infected plants immediately.\n2. Control whitefly populations aggressively.\n3. Use reflective mulches to repel whiteflies.\n4. No cure exists for infected plants.",
        "prevention": "Use resistant varieties (Ty-1, Ty-2 gene lines). Install insect-proof netting in greenhouses. Use yellow sticky traps. Maintain a host-free period between seasons.",
        "chemical_treatment": "Whitefly control: imidacloprid soil drench at transplanting, pyriproxyfen for nymph control, cyantraniliprole for adults. No chemical treats the virus itself.",
    },
    {
        "name": "Tomato - Mosaic Virus",
        "plant": "Tomato",
        "description": "Mottled light and dark green patches on leaves, sometimes leaves get distorted too. Spreads through contact, even dirty tools or hands can transfer it. ToMV virus.",
        "treatment": "1. Remove and destroy infected plants.\n2. Disinfect all tools and hands with milk solution or bleach.\n3. Do not compost infected material.\n4. No chemical cure available.",
        "prevention": "Use resistant varieties (Tm-2 gene). Wash hands with soap before handling plants. Disinfect tools between plants. Don't smoke near tomatoes (tobacco mosaic cross-infects).",
        "chemical_treatment": "No effective chemical treatments for viral infections. Focus on prevention. Some growers use milk sprays (1:9 ratio) as a folk remedy with limited evidence.",
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
