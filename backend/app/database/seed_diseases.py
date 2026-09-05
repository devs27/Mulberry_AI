from sqlalchemy.orm import Session
from app.models.disease_info import DiseaseInformation


def seed_disease_info(db: Session):
    diseases = [
        {
            "name": "Leaf Rust",
            "symptoms_en": "Small, orange-red or yellowish-brown pustules on the lower surface of leaves. Heavily infected leaves turn yellow, dry up, and fall off prematurely.",
            "symptoms_ta": "இலைகளின் கீழ் மேற்பரப்பில் சிறிய, ஆரஞ்சு-சிவப்பு அல்லது மஞ்சள்-பழுப்பு நிற கொப்புளங்கள் தோன்றும். பலத்த பாதிப்படைந்த இலைகள் மஞ்சளாகி, உலர்ந்து, முன்கூட்டியே உதிர்ந்துவிடும்.",
            "causes_en": "Fungal pathogen Cerotelium fici. Thrives in warm temperatures (22-30°C) and high humidity.",
            "causes_ta": "பூஞ்சை நோய்க்கிருமி செரோடெலியம் ஃபைசி (Cerotelium fici). சூடான வெப்பநிலை (22-30°C) மற்றும் அதிக ஈரப்பதத்தில் வளரும்.",
            "management_en": "Apply Carbendazim (0.1%) or Mancozeb (0.2%) spray. Maintain proper pruning and spacing to improve aeration.",
            "management_ta": "கார்பென்டாசிம் (0.1%) அல்லது மான்கோசெப் (0.2%) தெளிக்கவும். காற்றோட்டத்தை மேம்படுத்த சரியான கத்தரித்து இடைவெளியை பராமரிக்கவும்.",
            "prevention_en": "Collect and burn infected fallen leaves. Avoid overhead irrigation and ensure high field hygiene.",
            "prevention_ta": "பாதிக்கப்பட்ட உதிர்ந்த இலைகளை சேகரித்து எரிக்கவும். மேல்நிலை நீர்ப்பாசனத்தைத் தவிர்த்து, வயல் சுகாதாரத்தை உறுதிப்படுத்தவும்.",
            "disclaimer_en": "This is a general advisory. Consult local agriculture sericulture officers before spraying chemical fungicides.",
            "disclaimer_ta": "இது ஒரு பொதுவான ஆலோசனை. இரசாயன பூஞ்சைக் கொல்லிகளைத் தெளிப்பதற்கு முன் உள்ளூர் பட்டுப்புழு வளர்ப்பு அதிகாரிகளை அணுகவும்."
        },
        {
            "name": "Leaf Spot",
            "symptoms_en": "Dark brown circular spots on the leaf surface, which later become white/grey in the center. Causes leaves to turn yellow and drop.",
            "symptoms_ta": "இலை மேற்பரப்பில் கரும் பழுப்பு நிற வட்ட வடிவ புள்ளிகள் தோன்றி, பின்னர் மையத்தில் வெள்ளை/சாம்பல் நிறமாக மாறும். இலைகள் மஞ்சளாகி உதிரும்.",
            "causes_en": "Fungus Cercospora moricola. Spreads rapidly in warm, rainy seasons and high humidity.",
            "causes_ta": "பூஞ்சை செர்கோஸ்போரா மொரிகோலா (Cercospora moricola). வெப்பமான, மழைக்காலம் மற்றும் அதிக ஈரப்பதத்தில் வேகமாகப் பரவுகிறது.",
            "management_en": "Spray Carbendazim (0.1%) or Mancozeb (0.2%) at 12-15 days interval. Remove and burn diseased leaves.",
            "management_ta": "12-15 நாட்கள் இடைவெளியில் கார்பென்டாசிம் (0.1%) அல்லது மான்கோசெப் (0.2%) தெளிக்கவும். நோய்வாய்ப்பட்ட இலைகளை அகற்றி எரிக்கவும்.",
            "prevention_en": "Maintain clean weed-free garden, ensure wide spacing between plants for sunlight and wind penetration.",
            "prevention_ta": "களைகள் இல்லாத சுத்தமான தோட்டத்தை பராமரிக்கவும், சூரிய ஒளி மற்றும் காற்று உட்புக தாவரங்களுக்கு இடையே பரந்த இடைவெளியை உறுதி செய்யவும்.",
            "disclaimer_en": "Apply treatments strictly following local chemical usage guidelines.",
            "disclaimer_ta": "உள்ளூர் இரசாயன பயன்பாட்டு வழிகாட்டுதல்களை கண்டிப்பாக பின்பற்றி சிகிச்சைகளை பயன்படுத்தவும்."
        },
        {
            "name": "Powdery Mildew",
            "symptoms_en": "White powdery patches on the lower surface of leaves. Affected leaves curl, wither, and lose nutritional value for silkworms.",
            "symptoms_ta": "இலைகளின் கீழ் மேற்பரப்பில் வெள்ளை நிற மாவு போன்ற திட்டுகள் தோன்றும். பாதிக்கப்பட்ட இலைகள் சுருண்டு, வாடி, பட்டுப்புழுக்களுக்கான ஊட்டச்சத்து மதிப்பை இழக்கின்றன.",
            "causes_en": "Fungus Phyllactinia corylea. Favored by moderate temperatures (20-28°C) and humid shade.",
            "causes_ta": "பூஞ்சை ஃபிலாக்டினியா கோரிலியா (Phyllactinia corylea). மிதமான வெப்பநிலை (20-28°C) மற்றும் ஈரப்பதமான நிழலால் ஆதரிக்கப்படுகிறது.",
            "management_en": "Spray Dinocap (0.05%) or wettable sulfur (0.2%). Prune thick branches to increase sunlight exposure.",
            "management_ta": "டினோகாப் (0.05%) அல்லது நனையும் கந்தகம் (0.2%) தெளிக்கவும். சூரிய ஒளி படுவதை அதிகரிக்க அடர்த்தியான கிளைகளை கத்தரிக்கவும்.",
            "prevention_en": "Avoid planting in deep shade. Maintain correct pruning schedules.",
            "prevention_ta": "அடர்ந்த நிழலில் நடவு செய்வதைத் தவிர்க்கவும். சரியான கவாத்து அட்டவணையைப் பராமரிக்கவும்.",
            "disclaimer_en": "Observe a safe waiting period (plucking interval) before feeding leaves to silkworms after spraying.",
            "disclaimer_ta": "தெளித்த பிறகு பட்டுப்புழுக்களுக்கு இலைகளை ஊட்டுவதற்கு முன் பாதுகாப்பான காத்திருப்பு காலத்தை (இலை பறிக்கும் இடைவெளி) கடைபிடிக்கவும்."
        },
        {
            "name": "Bacterial Blight",
            "symptoms_en": "Water-soaked brown/black spots on leaves and stems, turning into black streaks. Leaves curl and rot.",
            "symptoms_ta": "இலைகள் மற்றும் தண்டுகளில் நீர் தேங்கிய பழுப்பு/கருப்பு புள்ளிகள் தோன்றி, கருப்பு கோடுகளாக மாறும். இலைகள் சுருண்டு அழுகும்.",
            "causes_en": "Bacterium Pseudomonas syringae pv. mori. Enters through wounds during high wind and rain.",
            "causes_ta": "பாக்டீரியம் சூடோமோனாஸ் சிரிங்கே பிவி. மோரி (Pseudomonas syringae pv. mori). பலத்த காற்று மற்றும் மழையின் போது காயங்கள் மூலம் நுழைகிறது.",
            "management_en": "Spray Streptomycin sulfate (0.01%) or Copper Oxychloride (0.2%). Clip off and burn infected twigs.",
            "management_ta": "ஸ்ட்ரெப்டோமைசின் சல்பேட் (0.01%) அல்லது காப்பர் ஆக்ஸிகுளோரைடு (0.2%) தெளிக்கவும். பாதிக்கப்பட்ட கிளைகளை வெட்டி எரிக்கவும்.",
            "prevention_en": "Disinfect pruning tools with spirit/bleach. Buy disease-free saplings.",
            "prevention_ta": "கவாத்து கருவிகளை ஸ்பிரிட்/பிளீச் கொண்டு கிருமி நீக்கம் செய்யவும். நோய் இல்லாத நாற்றுகளை வாங்கவும்.",
            "disclaimer_en": "Ensure chemical residue safety limits before harvesting leaves for silkworms.",
            "disclaimer_ta": "பட்டுப்புழுக்களுக்கு இலைகளை அறுவடை செய்வதற்கு முன் இரசாயன எச்ச பாதுகாப்பு வரம்புகளை உறுதி செய்யவும்."
        }
    ]

    for d in diseases:
        info = DiseaseInformation(**d)
        db.add(info)
    
    db.commit()
