const API_BASE_URL = "http://127.0.0.1:8000";

// ============================================================
// SECURITY — XSS PREVENTION
// ============================================================
function escapeHTML(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// ============================================================
// GLOBAL STATE
// ============================================================
let currentLang = localStorage.getItem("lang") || "en";
let currentThemePref = localStorage.getItem("mulberrycare-theme") || "system";
let activeHistoryFilter = "all";
let cachedDiagnoses = [];
let cachedWeatherRisk = null;
let cachedMarketListings = [];
let cachedMyListings = [];
let backendConnectionState = "checking";
let activeDiagnosisContext = null;
let chatSessionHistory = [];

// ============================================================
// TRANSLATION DICTIONARY
// ============================================================
const translations = {
  en: {
    // App
    app_title: "MulberryCare AI",
    app_subtitle: "AI-Powered Mulberry Health Assistant",
    app_tagline: "Smart Care for Better Mulberry Health",
    // Auth tabs
    login_tab: "Login",
    signup_tab: "Sign Up",
    login_title: "Welcome Back",
    signup_title: "Create Account",
    // Labels
    label_identifier: "Email or Phone Number",
    label_password: "Password",
    label_name: "Full Name",
    label_email: "Email Address (Optional)",
    label_phone: "Phone Number (Optional)",
    label_village: "Village / Location",
    label_variety: "Mulberry Variety",
    label_language: "Preferred Language",
    // Buttons
    btn_login: "Log In",
    btn_register: "Create Account",
    btn_logout: "Logout",
    btn_back: "Back",
    btn_diagnose: "Diagnose Leaf",
    btn_change_image: "Change photo",
    btn_ask_disease: "Ask about this disease",
    btn_search_listings: "Search Listings",
    btn_publish_listing: "Publish Listing",
    btn_mark_sold: "Mark as Sold",
    btn_sold: "Sold",
    btn_active: "Active",
    // Placeholders
    placeholder_identifier: "Enter email or phone number",
    placeholder_password: "Enter password",
    placeholder_name: "Enter your name",
    placeholder_email: "farmer@example.com",
    placeholder_phone: "e.g. 9876543210",
    placeholder_password_signup: "At least 6 characters",
    placeholder_village: "Enter your village name",
    placeholder_chat: "Ask about leaf health, pruning, irrigation...",
    // Dashboard greetings (time-aware)
    greeting_good_morning: "Good morning",
    greeting_good_afternoon: "Good afternoon",
    greeting_good_evening: "Good evening",
    greeting_good_night: "Good night",
    welcome_greeting: "Hello",
    variety_label: "Variety",
    village_label: "Village",
    variety_badge: "Variety",
    // Health Score
    health_score_label: "Farm Health Score",
    health_score_disclaimer: "Indicative score based on available platform data.",
    // Recommended Action
    recommended_action_title: "Recommended Action",
    // Snapshot
    snapshot_title: "Farm Snapshot",
    snapshot_crop: "Variety",
    snapshot_history: "Logs",
    snapshot_risk: "Risk",
    // Tiles
    tile_diagnose_title: "Diagnose Leaf",
    tile_diagnose_desc: "AI leaf disease detection",
    tile_history_title: "History",
    tile_history_desc: "View past diagnoses",
    tile_weather_title: "Weather Risk",
    tile_weather_desc: "Disease risk forecast",
    tile_chat_title: "AI Assistant",
    tile_chat_desc: "Farming guidance",
    tile_market_title: "Marketplace",
    tile_market_desc: "Buy & sell cocoons",
    tile_settings_title: "Settings",
    tile_settings_desc: "Profile & preferences",
    // Recent Activity
    recent_activity_title: "Recent Activity",
    activity_empty: "No recent activity.",
    activity_diagnosed: "Leaf diagnosed",
    activity_listing: "Cocoon listing published",
    activity_sold: "Listing marked as sold",
    // Diagnosis
    diagnose_title: "AI Leaf Disease Diagnosis",
    diagnose_desc: "Upload a clear mulberry leaf image for instant AI-assisted diagnosis. Drag & drop or tap to select.",
    choose_image: "Drop leaf photo here or tap to select",
    image_selected: "Image selected — ready",
    ai_assisted: "AI-ASSISTED",
    advisory_title: "Treatment Advisory:",
    confidence_label: "AI Confidence",
    confidence_badge: "Confidence",
    severity_badge: "Severity",
    // AI Loading
    processing_title: "Analysing leaf image...",
    step_upload: "Uploading leaf image...",
    step_quality: "Verifying image quality...",
    step_detect: "Running AI classification...",
    // Uncertain
    uncertain_title: "Diagnosis Uncertain",
    uncertain_warning: "AI confidence is below the safe threshold (70%). Please capture another clear image or consult an agricultural expert.",
    uncertain_try_again: "Try Another Image",
    uncertain_ask_assistant: "Ask MulberryCare",
    // History
    history_title: "Diagnosis History",
    no_records: "No diagnosis records found.",
    load_error: "Failed to load diagnosis history. Please reload.",
    loading_history: "Loading history...",
    history_empty_title: "No records yet",
    history_empty_desc: "Upload your first mulberry leaf to start monitoring crop health.",
    filter_all: "All",
    filter_healthy: "Healthy",
    filter_disease: "Diseases",
    filter_uncertain: "Uncertain",
    // Weather
    weather_risk_title: "Weather & Disease Risk",
    weather_risk_desc: "Simulated risk indicators based on historical climate profiles.",
    weather_temp: "Temperature",
    weather_humidity: "Humidity",
    weather_condition: "Condition",
    loading_weather: "Loading weather intelligence...",
    risk_label_high: "HIGH RISK",
    risk_label_moderate: "MODERATE RISK",
    risk_label_low: "LOW RISK",
    weather_demo_label: "DEMO / SIMULATED — Not real-time data",
    weather_explanation: "Risk awareness does not replace leaf diagnosis. Monitor field leaves regularly.",
    // Chat
    chat_title: "MulberryCare Assistant",
    chat_desc: "Bilingual RAG assistant grounded in curated sericulture knowledge.",
    chat_intro: "Hello! I am your MulberryCare assistant. How can I help you with mulberry cultivation or sericulture today?",
    chat_thinking: "MulberryCare is preparing your answer...",
    chat_err: "MulberryCare is temporarily unable to answer. Please try again.",
    safety_guided_badge: "Safety-guided",
    active_context_label: "Recent Diagnosis Context:",
    qa_today: "What should I do today?",
    qa_check_leaf: "Check a Leaf",
    qa_leaves_unhealthy: "My leaves look unhealthy",
    qa_when_irrigate: "When should I irrigate?",
    qa_found_pests: "I found pests",
    qa_how_prune: "How should I prune?",
    qa_worms_sick: "My silkworms look sick",
    qa_prepare_cocoons: "How do I prepare cocoons for sale?",
    sugg_pruning: "Pruning",
    sugg_irrigation: "Irrigation",
    sugg_disease: "Leaf Disease",
    sugg_fertilizer: "Fertilizer",
    sugg_silkworm: "Silkworm Care",
    sugg_selling: "Cocoon Selling",
    // Marketplace
    market_title: "Cocoon Marketplace",
    market_desc: "Connect directly with buyers and factories to sell your harvests.",
    market_tab_find: "🔎 Find Cocoons",
    market_tab_sell: "📦 Sell Cocoons",
    label_search_location: "Search by Location",
    label_search_variety: "Cocoon Variety",
    opt_all_varieties: "All Varieties",
    label_list_variety: "Cocoon Variety",
    label_list_price: "Price per kg (₹)",
    label_list_quantity: "Quantity (kg)",
    label_list_location: "Location / Village",
    label_list_phone: "Contact Phone",
    label_list_desc: "Description (Optional)",
    my_listings_title: "📋 My Cocoon Listings",
    contact_seller: "Contact Seller",
    contact_protected: "Seller contact protected",
    listed_on: "Listed",
    self_reported: "Self-reported",
    no_listings_found: "No cocoon listings found for your search.",
    marketplace_empty_title: "No listings found",
    marketplace_empty_desc: "Try another location or variety.",
    list_success: "Your cocoon listing has been published successfully.",
    list_err: "Unable to create listing. Please check input parameters.",
    contact_prefix: "Seller Phone",
    disc_quality_title: "Farmer-reported information",
    disc_quality_text: "Buyers should physically verify cocoon quality before transaction.",
    disc_price_title: "Price Disclaimer",
    disc_price_text: "Listed prices are farmer-provided and may change. MulberryCare does not guarantee price or transaction.",
    safe_trade_title: "Safe Trading",
    safe_trade_1: "Seller contact protected until buyer requests",
    safe_trade_2: "Listings are farmer-reported and self-certified",
    safe_trade_3: "Physically verify cocoon quality before purchase",
    safe_trade_4: "Check shell weight and pupal condition before transaction",
    safe_trade_5: "Confirm final price directly with the farmer",
    // Settings
    settings_title: "Profile & Settings",
    settings_profile_section: "Farmer Profile",
    settings_contact: "Contact",
    settings_language_section: "Language",
    settings_appearance_section: "Appearance",
    settings_theme_label: "Theme",
    // Theme
    theme_light: "☀ Light",
    theme_dark: "🌙 Dark",
    theme_system: "🖥 System",
    // Connection
    connecting: "Connecting...",
    connected: "Connected",
    not_reachable: "Offline",
    // Toasts
    toast_diagnosis_done: "Leaf diagnosis completed",
    toast_listing_published: "Cocoon listing published",
    toast_marked_sold: "Listing marked as sold",
    toast_network_error: "Connection interrupted. Please check your connection.",
    toast_diagnosis_uncertain: "Diagnosis uncertain — try a clearer image"
  },
  ta: {
    // App
    app_title: "மல்பெரிகேர் AI",
    app_subtitle: "AI-ஆற்றல் கொண்ட மல்பெரி ஆரோக்கிய உதவியாளர்",
    app_tagline: "மல்பெரி ஆரோக்கியத்திற்கான சிறந்த AI தொழில்நுட்பம்",
    // Auth
    login_tab: "உள்நுழை",
    signup_tab: "பதிவு செய்",
    login_title: "மீண்டும் வரவேற்கிறோம்",
    signup_title: "கணக்கை உருவாக்கு",
    label_identifier: "மின்னஞ்சல் அல்லது தொலைபேசி எண்",
    label_password: "கடவுச்சொல்",
    label_name: "முழு பெயர்",
    label_email: "மின்னஞ்சல் முகவரி (விருப்பத்திற்குரியது)",
    label_phone: "தொலைபேசி எண் (விருப்பத்திற்குரியது)",
    label_village: "கிராமம் / இருப்பிடம்",
    label_variety: "மல்பெரி வகை",
    label_language: "விருப்பமான மொழி",
    btn_login: "உள்நுழை",
    btn_register: "கணக்கை உருவாக்கு",
    btn_logout: "வெளியேறு",
    btn_back: "திரும்பு",
    btn_diagnose: "இலை கண்டறிதல்",
    btn_change_image: "படத்தை மாற்று",
    btn_ask_disease: "இந்த நோயைப் பற்றிக் கேளுங்கள்",
    btn_search_listings: "பட்டியல்களைத் தேடுங்கள்",
    btn_publish_listing: "பட்டியலை வெளியிடுங்கள்",
    btn_mark_sold: "விற்கப்பட்டதாக குறி",
    btn_sold: "விற்கப்பட்டது",
    btn_active: "செயலில் உள்ளது",
    placeholder_identifier: "மின்னஞ்சல் அல்லது தொலைபேசியை உள்ளிடவும்",
    placeholder_password: "கடவுச்சொல்லை உள்ளிடவும்",
    placeholder_name: "உங்கள் பெயரை உள்ளிடவும்",
    placeholder_email: "farmer@example.com",
    placeholder_phone: "உதாரணமாக 9876543210",
    placeholder_password_signup: "குறைந்தது 6 எழுத்துக்கள்",
    placeholder_village: "உங்கள் கிராமத்தின் பெயரை உள்ளிடவும்",
    placeholder_chat: "இலை ஆரோக்கியம், கவாத்து, நீர்ப்பாசனம் பற்றி கேளுங்கள்...",
    // Dashboard greetings (time-aware)
    greeting_good_morning: "காலை வணக்கம்",
    greeting_good_afternoon: "மதிய வணக்கம்",
    greeting_good_evening: "மாலை வணக்கம்",
    greeting_good_night: "இரவு வணக்கம்",
    welcome_greeting: "வணக்கம்",
    variety_label: "வகை",
    village_label: "கிராமம்",
    variety_badge: "வகை",
    health_score_label: "பண்ணை ஆரோக்கிய மதிப்பெண்",
    health_score_disclaimer: "கிடைக்கக்கூடிய தரவின் அடிப்படையில் குறிப்பிட்டைய மதிப்பெண்.",
    recommended_action_title: "பரிந்துரைக்கப்பட்ட நடவடிக்கை",
    snapshot_title: "பண்ணை சுருக்கம்",
    snapshot_crop: "வகை",
    snapshot_history: "பதிவுகள்",
    snapshot_risk: "அபாயம்",
    tile_diagnose_title: "இலை கண்டறிதல்",
    tile_diagnose_desc: "AI இலை நோய் கண்டறிதல்",
    tile_history_title: "வரலாறு",
    tile_history_desc: "முந்தைய முடிவுகள்",
    tile_weather_title: "வானிலை அபாயம்",
    tile_weather_desc: "நோய் அபாய முன்னறிவிப்பு",
    tile_chat_title: "AI உதவியாளர்",
    tile_chat_desc: "விவசாய வழிகாட்டல்",
    tile_market_title: "சந்தை",
    tile_market_desc: "பட்டுக்கூடு வர்த்தகம்",
    tile_settings_title: "அமைப்புகள்",
    tile_settings_desc: "சுயவிவரம் மற்றும் விருப்பங்கள்",
    recent_activity_title: "சமீபத்திய செயல்பாடு",
    activity_empty: "சமீபத்திய செயல்பாடு எதுவும் இல்லை.",
    activity_diagnosed: "இலை கண்டறியப்பட்டது",
    activity_listing: "பட்டுக்கூடு பட்டியல் வெளியிடப்பட்டது",
    activity_sold: "பட்டியல் விற்கப்பட்டதாக குறிக்கப்பட்டது",
    diagnose_title: "AI இலை நோய் கண்டறிதல்",
    diagnose_desc: "உடனடி AI நோய் கண்டறிதலுக்கு ஒரு தெளிவான மல்பெரி இலை படத்தை பதிவேற்றவும்.",
    choose_image: "இலை படத்தை இங்கே இழுத்து விடவும் அல்லது தேர்ந்தெடுக்கவும்",
    image_selected: "படம் தேர்ந்தெடுக்கப்பட்டது",
    ai_assisted: "AI-ஆதரிக்கப்பட்டது",
    advisory_title: "சிகிச்சை ஆலோசனை:",
    confidence_label: "AI நம்பிக்கை",
    confidence_badge: "நம்பிக்கை",
    severity_badge: "தீவிரம்",
    processing_title: "இலை படத்தை பகுப்பாய்வு செய்கிறது...",
    step_upload: "இலை படத்தை பதிவேற்றுகிறது...",
    step_quality: "படத்தின் தரத்தை சரிபார்க்கிறது...",
    step_detect: "AI வகைப்பாட்டை இயக்குகிறது...",
    uncertain_title: "கண்டறிதல் நிச்சயமற்றது",
    uncertain_warning: "AI நம்பிக்கை பாதுகாப்பான வரம்பிற்கு (70%) கீழே உள்ளது. மற்றொரு தெளிவான படத்தை எடுக்கவும் அல்லது விவசாய நிபுணரை அணுகவும்.",
    uncertain_try_again: "மற்றொரு படத்தை முயற்சி",
    uncertain_ask_assistant: "மல்பெரிகேரைக் கேளுங்கள்",
    history_title: "நோய் கண்டறிதல் வரலாறு",
    no_records: "நோய் கண்டறிதல் பதிவுகள் எதுவும் இல்லை.",
    load_error: "வரலாற்றை ஏற்றுவதில் தோல்வி. மீண்டும் முயற்சிக்கவும்.",
    loading_history: "வரலாற்றை ஏற்றுகிறது...",
    history_empty_title: "பதிவுகள் இல்லை",
    history_empty_desc: "பயிர் ஆரோக்கியத்தை கண்காணிக்க உங்கள் முதல் இலையை பதிவேற்றவும்.",
    filter_all: "அனைத்தும்",
    filter_healthy: "ஆரோக்கியமான",
    filter_disease: "நோய்கள்",
    filter_uncertain: "நிச்சயமற்றது",
    weather_risk_title: "வானிலை மற்றும் நோய் அபாயம்",
    weather_risk_desc: "வரலாற்று காலநிலை சுயவிவரங்களின் அடிப்படையில் உருவகப்படுத்தப்பட்ட அபாய குறிகாட்டிகள்.",
    weather_temp: "வெப்பநிலை",
    weather_humidity: "ஈரப்பதம்",
    weather_condition: "வானிலை",
    loading_weather: "வானிலை தகவல்களை ஏற்றுகிறது...",
    risk_label_high: "அதிக அபாயம்",
    risk_label_moderate: "மிதமான அபாயம்",
    risk_label_low: "குறைந்த அபாயம்",
    weather_demo_label: "டெமோ / உருவகப்படுத்தப்பட்டது — நிகழ் நேர தரவல்ல",
    weather_explanation: "அபாய விழிப்புணர்வு இலை நோய் கண்டறிதலை மாற்றாது. வயல் இலைகளை தொடர்ந்து கண்காணிக்கவும்.",
    chat_title: "மல்பெரிகேர் உதவியாளர்",
    chat_desc: "மல்பெரி சாகுபடி மற்றும் பட்டுப்புழு வளர்ப்பு சார்ந்த இருமொழி AI உதவியாளர்.",
    chat_intro: "வணக்கம்! நான் உங்கள் மல்பெரிகேர் உதவியாளர். மல்பெரி சாகுபடி அல்லது பட்டுப்புழு வளர்ப்பில் உங்களுக்கு இன்று நான் எவ்வாறு உதவ முடியும்?",
    chat_thinking: "மல்பெரிகேர் பதில் தயாரித்துக் கொண்டிருக்கிறது...",
    chat_err: "மல்பெரிகேர் தற்போது பதிலளிக்க முடியவில்லை. மீண்டும் முயற்சிக்கவும்.",
    safety_guided_badge: "பாதுகாப்பு வழிகாட்டல்",
    active_context_label: "சமீபத்திய கண்டறிதல் சூழல்:",
    qa_today: "இன்று என்ன செய்ய வேண்டும்?",
    qa_check_leaf: "இலையை பரிசோதிக்கவும்",
    qa_leaves_unhealthy: "இலைகள் ஆரோக்கியமற்றதாக உள்ளன",
    qa_when_irrigate: "எப்போது நீர் பாய்ச்ச வேண்டும்?",
    qa_found_pests: "பூச்சி தாக்குதல் தென்படுகிறது",
    qa_how_prune: "எவ்வாறு கவாத்து செய்ய வேண்டும்?",
    qa_worms_sick: "பட்டுப்புழுக்கள் நோய்வாய்ப்பட்டுள்ளன",
    qa_prepare_cocoons: "கூடுகளை விற்பனைக்கு தயார் செய்வது எப்படி?",
    sugg_pruning: "கவாத்து",
    sugg_irrigation: "நீர்ப்பாசனம்",
    sugg_disease: "இலை நோய்",
    sugg_fertilizer: "உரங்கள்",
    sugg_silkworm: "புழு வளர்ப்பு",
    sugg_selling: "கூடு விற்பனை",
    market_title: "பட்டுக்கூடு சந்தை",
    market_desc: "விற்பனையாளர்கள் மற்றும் வாங்குபவர்களை நேரடியாக இணைக்கும் சந்தை.",
    market_tab_find: "🔎 பட்டுக்கூடு தேடு",
    market_tab_sell: "📦 பட்டுக்கூடு விற்பனை",
    label_search_location: "இருப்பிடம் மூலம் தேடுங்கள்",
    label_search_variety: "பட்டுக்கூடு வகை",
    opt_all_varieties: "அனைத்து வகைகள்",
    label_list_variety: "பட்டுக்கூடு வகை",
    label_list_price: "ஒரு கிலோ விலை (₹)",
    label_list_quantity: "அளவு (கிலோ)",
    label_list_location: "இருப்பிடம் / கிராமம்",
    label_list_phone: "தொடர்பு எண்",
    label_list_desc: "விளக்கம் (விருப்பத்திற்குரியது)",
    my_listings_title: "📋 எனது பட்டுக்கூடு பட்டியல்கள்",
    contact_seller: "தொடர்பு கொள்ளவும்",
    contact_protected: "விற்பனையாளர் தொடர்பு பாதுகாக்கப்பட்டுள்ளது",
    listed_on: "பதிவுசெய்யப்பட்டது",
    self_reported: "சுய-அறிவிப்பு",
    no_listings_found: "உங்கள் தேடலுக்கு எந்த பட்டுக்கூடு பட்டியல்களும் கிடைக்கவில்லை.",
    marketplace_empty_title: "பட்டியல்கள் இல்லை",
    marketplace_empty_desc: "மற்றொரு இருப்பிடம் அல்லது வகையை முயற்சிக்கவும்.",
    list_success: "உங்கள் பட்டுக்கூடு பட்டியல் வெற்றிகரமாக வெளியிடப்பட்டது.",
    list_err: "பட்டியலை வெளியிட முடியவில்லை. உள்ளீட்டு அளவுகளைச் சரிபார்க்கவும்.",
    contact_prefix: "விற்பனையாளர் எண்",
    disc_quality_title: "விவசாயி-அறிவித்த தகவல்",
    disc_quality_text: "வாங்குபவர்கள் பரிவர்த்தனைக்கு முன் பட்டுக்கூடு தரத்தை நேரில் சரிபார்க்க வேண்டும்.",
    disc_price_title: "விலை பொறுப்புத் துறப்பு",
    disc_price_text: "குறிப்பிடப்பட்ட விலைகள் விவசாயிகளால் வழங்கப்பட்டவை மற்றும் மாறக்கூடும்.",
    safe_trade_title: "பாதுகாப்பான வர்த்தகம்",
    safe_trade_1: "வாங்குபவர் கோரும் வரை விற்பனையாளர் தொடர்பு பாதுகாக்கப்படும்",
    safe_trade_2: "பட்டியல்கள் விவசாயிகளால் சுய-சான்றளிக்கப்பட்டவை",
    safe_trade_3: "வாங்குவதற்கு முன் பட்டுக்கூடு தரத்தை நேரில் சரிபார்க்கவும்",
    safe_trade_4: "பரிவர்த்தனைக்கு முன் ஓடு எடை மற்றும் கூட்டுப்புழு நிலையை சரிபார்க்கவும்",
    safe_trade_5: "விவசாயியிடம் நேரடியாக இறுதி விலையை உறுதிப்படுத்தவும்",
    settings_title: "சுயவிவரம் மற்றும் அமைப்புகள்",
    settings_profile_section: "விவசாயி சுயவிவரம்",
    settings_contact: "தொடர்பு",
    settings_language_section: "மொழி",
    settings_appearance_section: "தோற்றம்",
    settings_theme_label: "தீம்",
    theme_light: "☀ ஒளி",
    theme_dark: "🌙 இருட்டு",
    theme_system: "🖥 அமைப்பு",
    connecting: "இணைக்கிறது...",
    connected: "இணைக்கப்பட்டது",
    not_reachable: "ஆஃப்லைன்",
    toast_diagnosis_done: "இலை கண்டறிதல் முடிந்தது",
    toast_listing_published: "பட்டுக்கூடு பட்டியல் வெளியிடப்பட்டது",
    toast_marked_sold: "பட்டியல் விற்கப்பட்டதாக குறிக்கப்பட்டது",
    toast_network_error: "இணைப்பு துண்டிக்கப்பட்டது. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.",
    toast_diagnosis_uncertain: "கண்டறிதல் நிச்சயமற்றது — தெளிவான படம் முயற்சிக்கவும்"
  }
};

// ============================================================
// THEME ENGINE
// ============================================================
function initTheme() {
  const saved = localStorage.getItem("mulberrycare-theme") || "system";
  currentThemePref = saved;
  applyTheme(saved);
  updateThemeButtons();
}

function applyTheme(pref) {
  let effectiveTheme = pref;
  if (pref === "system") {
    effectiveTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  document.documentElement.setAttribute("data-theme", effectiveTheme);
  const icon = document.getElementById("theme-icon");
  if (icon) icon.textContent = effectiveTheme === "dark" ? "☀" : "🌙";
}

function setTheme(pref) {
  currentThemePref = pref;
  localStorage.setItem("mulberrycare-theme", pref);
  applyTheme(pref);
  updateThemeButtons();
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");
  setTheme(current === "dark" ? "light" : "dark");
}

function updateThemeButtons() {
  ["light","dark","system"].forEach(t => {
    const btn = document.getElementById(`theme-opt-${t}`);
    if (btn) btn.classList.toggle("active", currentThemePref === t);
  });
}

// Listen for system theme changes when pref is "system"
window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
  if (currentThemePref === "system") applyTheme("system");
});

// ============================================================
// TOAST NOTIFICATION SYSTEM
// ============================================================
function showToast(message, type = "success", duration = 4500) {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const icons = { success: "✓", warning: "⚠", error: "✕", info: "ⓘ" };

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.setAttribute("role", "status");
  toast.innerHTML = `
    <span class="toast-icon" aria-hidden="true">${icons[type] || icons.info}</span>
    <span class="toast-text">${escapeHTML(message)}</span>
    <button class="toast-close" onclick="dismissToast(this.parentElement)" aria-label="Dismiss">✕</button>
  `;
  container.appendChild(toast);

  setTimeout(() => dismissToast(toast), duration);
}

function dismissToast(toast) {
  if (!toast || toast.classList.contains("removing")) return;
  toast.classList.add("removing");
  setTimeout(() => { if (toast.parentElement) toast.parentElement.removeChild(toast); }, 300);
}

// ============================================================
// TIME-AWARE GREETING
// ============================================================
function getTimeGreeting() {
  const hour = new Date().getHours();
  if (hour >= 5  && hour < 12) return "greeting_good_morning";
  if (hour >= 12 && hour < 17) return "greeting_good_afternoon";
  if (hour >= 17 && hour < 21) return "greeting_good_evening";
  return "greeting_good_night";
}

function applyGreeting() {
  const greetingSpan = document.getElementById("greeting-text");
  if (!greetingSpan) return;
  const key = getTimeGreeting();
  greetingSpan.textContent = translations[currentLang][key] || translations.en[key];
}

// ============================================================
// BACKEND HEALTH CHECK
// ============================================================
async function checkHealth() {
  const statusEl = document.getElementById("status");
  const statusBar = document.getElementById("status-bar");
  try {
    const res = await fetch(`${API_BASE_URL}/api/health`);
    await res.json();
    backendConnectionState = "connected";
    if (statusEl) statusEl.textContent = translations[currentLang].connected;
    if (statusBar) statusBar.className = "connection-status ok";
  } catch (err) {
    backendConnectionState = "error";
    if (statusEl) statusEl.textContent = translations[currentLang].not_reachable;
    if (statusBar) statusBar.className = "connection-status error";
  }
}

// ============================================================
// AUTH TABS
// ============================================================
function switchTab(tab) {
  const loginForm = document.getElementById("login-form");
  const signupForm = document.getElementById("signup-form");
  const tabLogin = document.getElementById("tab-login");
  const tabSignup = document.getElementById("tab-signup");

  if (tab === "login") {
    loginForm.classList.remove("hidden");
    signupForm.classList.add("hidden");
    tabLogin.classList.add("active");
    tabSignup.classList.remove("active");
    tabLogin.setAttribute("aria-selected", "true");
    tabSignup.setAttribute("aria-selected", "false");
  } else {
    loginForm.classList.add("hidden");
    signupForm.classList.remove("hidden");
    tabLogin.classList.remove("active");
    tabSignup.classList.add("active");
    tabLogin.setAttribute("aria-selected", "false");
    tabSignup.setAttribute("aria-selected", "true");
  }
}

// ============================================================
// SHOW / HIDE PASSWORD
// ============================================================
function togglePasswordVisibility(fieldId, btn) {
  const input = document.getElementById(fieldId);
  if (!input) return;
  const isHidden = input.type === "password";
  input.type = isHidden ? "text" : "password";
  btn.textContent = isHidden ? "🙈" : "👁";
  btn.setAttribute("aria-label", isHidden ? "Hide password" : "Show password");
}

// ============================================================
// AUTH UI STATE
// ============================================================
function updateAuthUI() {
  const token = localStorage.getItem("token");
  const userJson = localStorage.getItem("user");
  const authView = document.getElementById("auth-view");
  const dashboardView = document.getElementById("dashboard-view");

  if (token && userJson) {
    const user = JSON.parse(userJson);

    // Set profile info
    const farmerNameEl = document.getElementById("farmer-name");
    const farmerVarietyEl = document.getElementById("farmer-variety");
    const farmerVillageEl = document.getElementById("farmer-village");
    if (farmerNameEl) farmerNameEl.textContent = user.name;
    if (farmerVarietyEl) farmerVarietyEl.textContent = user.preferred_variety || "S36";
    if (farmerVillageEl) farmerVillageEl.textContent = user.village || "—";
    applyGreeting(); // set time-aware greeting (morning / afternoon / evening / night)

    // Pre-fill sell form
    const listPhone = document.getElementById("list-phone");
    const listLocation = document.getElementById("list-location");
    if (listPhone) listPhone.value = user.phone || "";
    if (listLocation) listLocation.value = user.village || "";

    // Apply user's saved language
    if (user.preferred_language && (user.preferred_language === "en" || user.preferred_language === "ta")) {
      currentLang = user.preferred_language;
      localStorage.setItem("lang", currentLang);
    }

    authView.classList.add("hidden");
    dashboardView.classList.remove("hidden");
    const topMenuBar = document.getElementById("top-menu-bar");
    if (topMenuBar) topMenuBar.classList.remove("hidden");

    // Reset to default panel
    switchDashboardView("diagnose");

    // Reset diagnosis state
    const diagResult = document.getElementById("diagnosis-result");
    const uploadPreview = document.getElementById("upload-preview-container");
    const loadingSteps = document.getElementById("loading-steps-container");
    const uploadForm = document.getElementById("upload-form");
    const fileChosenText = document.getElementById("file-chosen-text");
    if (diagResult) diagResult.classList.add("hidden");
    if (uploadPreview) uploadPreview.classList.add("hidden");
    if (loadingSteps) loadingSteps.classList.add("hidden");
    if (uploadForm) uploadForm.reset();
    if (fileChosenText) fileChosenText.textContent = translations[currentLang].choose_image;

    // Reset chat
    const transcript = document.getElementById("chat-transcript");
    const chatForm = document.getElementById("chat-form");
    if (transcript) {
      transcript.innerHTML = `
        <div class="chat-msg msg-assistant">
          <div class="msg-avatar" aria-hidden="true">🌿</div>
          <div class="msg-bubble">
            <p>${translations[currentLang].chat_intro}</p>
          </div>
        </div>
      `;
    }
    if (chatForm) chatForm.reset();

    // Update settings page fields
    updateSettingsPage();

    // Kick off data loads
    loadHistory();
    loadWeatherRisk();
    searchMarketListings();
    loadMyListings();
  } else {
    authView.classList.remove("hidden");
    dashboardView.classList.add("hidden");
    const topMenuBar = document.getElementById("top-menu-bar");
    if (topMenuBar) topMenuBar.classList.add("hidden");
    document.body.setAttribute("data-page", "auth");
  }

  applyLanguage(currentLang);
}

// ============================================================
// SPA NAVIGATION
// ============================================================
function switchDashboardView(viewName) {
  document.body.setAttribute("data-page", viewName);
  const allViews = ["diagnose", "history", "weather", "chat", "market", "settings"];

  allViews.forEach(v => {
    // Top Navigation Menu Items
    const topNavBtn = document.getElementById(`top-nav-${v}`);
    if (topNavBtn) {
      const isActive = v === viewName;
      topNavBtn.classList.toggle("active", isActive);
      topNavBtn.setAttribute("aria-selected", isActive ? "true" : "false");
    }

    // Sidebar Tiles (if any)
    const tile = document.getElementById(`tile-${v}`);
    if (tile) {
      const isActive = v === viewName;
      tile.classList.toggle("active", isActive);
      tile.setAttribute("aria-pressed", isActive ? "true" : "false");
    }

    // Content Panels
    const panel = document.getElementById(`panel-${v}`);
    if (panel) {
      const isActive = v === viewName;
      panel.classList.toggle("hidden", !isActive);
      if (isActive) panel.classList.add("active-panel");
    }
  });

  // Scroll into view on mobile
  if (window.innerWidth <= 840) {
    const container = document.getElementById("dashboard-active-view-container");
    if (container) container.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

// ============================================================
// APPLY LANGUAGE
// ============================================================
function applyLanguage(lang) {
  currentLang = lang;
  localStorage.setItem("lang", lang);

  // Update data-i18n elements
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (translations[lang] && translations[lang][key] !== undefined) {
      el.textContent = translations[lang][key];
    }
  });

  // Update placeholders
  const placeholderMap = {
    "login-identifier": "placeholder_identifier",
    "login-password": "placeholder_password",
    "signup-name": "placeholder_name",
    "signup-email": "placeholder_email",
    "signup-phone": "placeholder_phone",
    "signup-village": "placeholder_village",
    "signup-password": "placeholder_password_signup",
    "chat-input": "placeholder_chat"
  };
  Object.entries(placeholderMap).forEach(([id, key]) => {
    const el = document.getElementById(id);
    if (el && translations[lang][key]) el.placeholder = translations[lang][key];
  });

  // Connection status
  const statusEl = document.getElementById("status");
  const statusBar = document.getElementById("status-bar");
  if (statusEl && statusBar) {
    if (backendConnectionState === "connected") {
      statusEl.textContent = translations[lang].connected;
      statusBar.className = "connection-status ok";
    } else if (backendConnectionState === "error") {
      statusEl.textContent = translations[lang].not_reachable;
      statusBar.className = "connection-status error";
    } else {
      statusEl.textContent = translations[lang].connecting;
    }
  }

  // Language button highlights
  const enLink = document.getElementById("lang-en");
  const taLink = document.getElementById("lang-ta");
  if (enLink && taLink) {
    enLink.classList.toggle("active", lang === "en");
    taLink.classList.toggle("active", lang === "ta");
    enLink.setAttribute("aria-pressed", lang === "en" ? "true" : "false");
    taLink.setAttribute("aria-pressed", lang === "ta" ? "true" : "false");
  }

  // Settings language buttons
  const settingsEnBtn = document.getElementById("settings-lang-en");
  const settingsTaBtn = document.getElementById("settings-lang-ta");
  if (settingsEnBtn) settingsEnBtn.classList.toggle("active", lang === "en");
  if (settingsTaBtn) settingsTaBtn.classList.toggle("active", lang === "ta");

  // Reset file chosen text if no file
  const fileChosenText = document.getElementById("file-chosen-text");
  const fileInput = document.getElementById("leaf-file");
  if (fileChosenText && (!fileInput || !fileInput.files || fileInput.files.length === 0)) {
    fileChosenText.textContent = translations[lang].choose_image;
  }

  // Translate chat intro if only one message
  const transcript = document.getElementById("chat-transcript");
  if (transcript && transcript.children.length === 1) {
    transcript.innerHTML = `
      <div class="chat-msg msg-assistant">
        <div class="msg-avatar" aria-hidden="true">🌿</div>
        <div class="msg-bubble">
          <p>${translations[lang].chat_intro}</p>
        </div>
      </div>
    `;
  }

  // Re-render all cached data
  renderHistory(getFilteredDiagnoses());
  renderWeatherRisk(cachedWeatherRisk);
  renderMarketListings(cachedMarketListings);
  renderMyListings(cachedMyListings);
  updateFarmSnapshot();
  updateSettingsPage();
}

function setLanguage(lang) {
  applyLanguage(lang);
}

// ============================================================
// SETTINGS PAGE
// ============================================================
function updateSettingsPage() {
  const userJson = localStorage.getItem("user");
  if (!userJson) return;
  const user = JSON.parse(userJson);

  const nameEl = document.getElementById("settings-name");
  const contactEl = document.getElementById("settings-contact");
  const villageEl = document.getElementById("settings-village");
  const varietyEl = document.getElementById("settings-variety");

  if (nameEl) nameEl.textContent = user.name || "—";
  if (contactEl) contactEl.textContent = user.email || user.phone || "—";
  if (villageEl) villageEl.textContent = user.village || "—";
  if (varietyEl) varietyEl.textContent = user.preferred_variety || "—";

  updateThemeButtons();

  const settingsEnBtn = document.getElementById("settings-lang-en");
  const settingsTaBtn = document.getElementById("settings-lang-ta");
  if (settingsEnBtn) settingsEnBtn.classList.toggle("active", currentLang === "en");
  if (settingsTaBtn) settingsTaBtn.classList.toggle("active", currentLang === "ta");
}

// ============================================================
// FARM SNAPSHOT
// ============================================================
function updateFarmSnapshot() {
  const varietyEl = document.getElementById("snapshot-val-variety");
  const historyEl = document.getElementById("snapshot-val-history");
  const riskEl = document.getElementById("snapshot-val-risk");
  const farmerVariety = document.getElementById("farmer-variety");

  if (varietyEl && farmerVariety) varietyEl.textContent = farmerVariety.textContent || "S36";
  if (historyEl) historyEl.textContent = String(cachedDiagnoses.length);

  if (riskEl && cachedWeatherRisk && cachedWeatherRisk.risks && cachedWeatherRisk.risks.length > 0) {
    const primaryRisk = cachedWeatherRisk.risks[0].risk_level;
    const label = currentLang === "ta"
      ? (primaryRisk === "High" ? translations.ta.risk_label_high
         : primaryRisk === "Moderate" ? translations.ta.risk_label_moderate
         : translations.ta.risk_label_low)
      : (primaryRisk === "High" ? "High" : primaryRisk === "Moderate" ? "Moderate" : "Low");
    riskEl.textContent = label;
    riskEl.className = `snapshot-value risk-tag-${primaryRisk.toLowerCase()}`;
  }
}

// ============================================================
// FARM HEALTH SCORE
// ============================================================
function computeFarmHealthScore() {
  // Base score from diagnosis history
  let score = 50;

  if (cachedDiagnoses.length > 0) {
    const recent = cachedDiagnoses.slice(0, 5);
    const healthyCount = recent.filter(d => d.disease.toLowerCase().includes("healthy")).length;
    const certainCount = recent.filter(d => !d.is_uncertain).length;
    const avgConf = recent.reduce((s, d) => s + d.confidence, 0) / recent.length;

    score = Math.round(
      (healthyCount / recent.length) * 35 +
      (certainCount / recent.length) * 20 +
      (avgConf) * 25 +
      20
    );
  }

  // Penalise for weather risk
  if (cachedWeatherRisk && cachedWeatherRisk.risks) {
    const highCount = cachedWeatherRisk.risks.filter(r => r.risk_level === "High").length;
    const modCount = cachedWeatherRisk.risks.filter(r => r.risk_level === "Moderate").length;
    score -= highCount * 10 + modCount * 5;
  }

  score = Math.max(5, Math.min(100, score));
  return score;
}

function updateHealthScore() {
  const score = computeFarmHealthScore();
  const hasData = cachedDiagnoses.length > 0 || cachedWeatherRisk;
  const valueEl = document.getElementById("health-score-value");
  const circleEl = document.getElementById("score-circle");
  const statusEl = document.getElementById("score-status-text");

  if (!hasData) {
    if (valueEl) valueEl.textContent = "—";
    if (statusEl) statusEl.textContent = "No data yet";
    return;
  }

  if (valueEl) valueEl.textContent = String(score);

  // Band labels
  const isExcellent = score >= 85;
  const isGood      = score >= 70 && score < 85;
  const isMid       = score >= 40 && score < 70;
  const isBad       = score < 40;

  const labels = {
    en: { excellent: "Excellent 🟢", good: "Good 🟢", fair: "Fair 🟠", bad: "Needs Attention 🔴" },
    ta: { excellent: "சிறப்பு 🟢", good: "நல்லது 🟢", fair: "ஒரளவு 🟠", bad: "கவனம் தேவை 🔴" }
  };
  const l = labels[currentLang] || labels.en;
  const statusText = isExcellent ? l.excellent : isGood ? l.good : isMid ? l.fair : l.bad;
  if (statusEl) statusEl.textContent = statusText;

  // Arc colour
  const color = (isExcellent || isGood) ? "var(--success)" : isMid ? "var(--warning)" : "var(--danger)";
  if (circleEl) {
    circleEl.style.setProperty("--score-pct", String(score));
    circleEl.style.background = `conic-gradient(${color} ${score}%, var(--bg-secondary) 0%)`;
  }

  // Colour bar segment highlight
  const segs = document.querySelectorAll(".score-bar-seg");
  if (segs.length === 3) {
    segs[0].classList.toggle("active", isBad);
    segs[1].classList.toggle("active", isMid);
    segs[2].classList.toggle("active", isExcellent || isGood);
  }
}

// ============================================================
// RECOMMENDED ACTION
// ============================================================
let actionDismissed = false;

function dismissRecommendedAction() {
  actionDismissed = true;
  const card = document.getElementById("recommended-action-card");
  if (card) card.classList.add("hidden");
}

function askAIAboutDisease(diseaseName) {
  switchDashboardView("chat");
  const input = document.getElementById("chat-input");
  if (input) {
    const query = currentLang === "ta"
      ? `முசுக்கட்டை இலையில் ${diseaseName} நோயை எவ்வாறு கட்டுப்படுத்துவது?`
      : `How to treat and prevent ${diseaseName} in mulberry leaves?`;
    input.value = query;
    input.focus();
  }
}

function updateRecommendedAction() {
  const card = document.getElementById("recommended-action-card");
  const text = document.getElementById("recommended-action-text");
  const btn = document.getElementById("recommended-action-btn");
  const secBtn = document.getElementById("recommended-action-secondary-btn");
  const badge = document.getElementById("alert-severity-badge");

  if (!card || !text || actionDismissed) return;

  let message = null;
  let btnTarget = "diagnose";
  let btnLabel = currentLang === "ta" ? "🌿 இலை ஆரோக்கியம் சரிபார்க்கவும்" : "🌿 Check Leaf Health";
  let secDisease = null;
  let severityText = currentLang === "ta" ? "உயர் அபாயம்" : "High Risk";
  let isAlert = true;

  if (cachedWeatherRisk && cachedWeatherRisk.risks) {
    const highRisk = cachedWeatherRisk.risks.find(r => r.risk_level === "High");
    if (highRisk) {
      const name = currentLang === "ta" ? highRisk.disease_ta : highRisk.disease;
      message = currentLang === "ta"
        ? `${name} அபாயம் தற்போது அதிகமாக உள்ளது.`
        : `${name} risk is currently HIGH.`;
      btnTarget = "diagnose";
      secDisease = highRisk.disease;
    }
  }

  if (!message && cachedDiagnoses.length > 0) {
    const last = cachedDiagnoses[0];
    if (last.is_uncertain || last.confidence < 0.70) {
      message = currentLang === "ta"
        ? "உங்கள் கடைசி கண்டறிதல் நிச்சயமற்றது. தெளிவான படத்தை பதிவேற்றவும்."
        : "Your last diagnosis was uncertain. Upload a clearer image.";
      btnTarget = "diagnose";
      severityText = currentLang === "ta" ? "கவனம் தேவை" : "Needs Review";
    } else if (last.disease !== "Healthy") {
      message = currentLang === "ta"
        ? `கடைசி கண்டறிதல்: ${last.disease}. சிகிச்சை முறைகளை பார்க்கவும்.`
        : `Recent diagnosis: ${last.disease}. View treatment guidance.`;
      btnTarget = "history";
      btnLabel = currentLang === "ta" ? "📋 வரலாற்றைப் பார்க்கவும்" : "📋 View Treatment";
      secDisease = last.disease;
      severityText = currentLang === "ta" ? "சிகிச்சை தேவை" : "Treatment Required";
    }
  }

  if (!message && cachedDiagnoses.length === 0) {
    message = currentLang === "ta"
      ? "உங்கள் பயிர் ஆரோக்கியத்தை கண்காணிக்க தொடங்கவும்."
      : "Start monitoring your crop health today.";
    btnTarget = "diagnose";
    isAlert = false;
    severityText = currentLang === "ta" ? "சாதகமானது" : "Normal";
  }

  if (message) {
    text.textContent = message;
    if (btn) {
      btn.innerHTML = `<span aria-hidden="true">${btnLabel.split(' ')[0]}</span> ${btnLabel.substring(btnLabel.indexOf(' ') + 1)}`;
      btn.onclick = () => switchDashboardView(btnTarget);
    }
    if (secBtn) {
      if (secDisease) {
        secBtn.innerHTML = `<span aria-hidden="true">💬</span> ${currentLang === "ta" ? "AI உதவி கேட்கவும்" : "Ask AI Assistant"}`;
        secBtn.onclick = () => askAIAboutDisease(secDisease);
        secBtn.classList.remove("hidden");
      } else {
        secBtn.classList.add("hidden");
      }
    }
    if (badge) {
      badge.textContent = severityText;
    }
    card.classList.remove("hidden");
    card.className = `alert-card${isAlert ? "" : " alert-success"}`;
  } else {
    card.classList.add("hidden");
  }
}

// ============================================================
// RECENT ACTIVITY
// ============================================================
function renderRecentActivity() {
  const container = document.getElementById("recent-activity-list");
  if (!container) return;

  const activities = [];

  cachedDiagnoses.slice(0, 3).forEach(d => {
    const isHealthy = d.disease.toLowerCase().includes("healthy");
    const isUncertain = d.is_uncertain || d.confidence < 0.70;
    const icon = isUncertain ? "⚠" : isHealthy ? "🌿" : "🔴";
    const label = `${translations[currentLang].activity_diagnosed}: ${d.disease}`;
    const date = new Date(d.timestamp);
    activities.push({
      icon,
      text: label,
      time: date.toLocaleDateString(currentLang === "ta" ? "ta-IN" : "en-GB", { day: "numeric", month: "short" })
    });
  });

  cachedMyListings.slice(0, 2).forEach(l => {
    const icon = l.status === "sold" ? "✅" : "📦";
    const label = l.status === "sold"
      ? `${translations[currentLang].activity_sold}: ${l.variety}`
      : `${translations[currentLang].activity_listing}: ${l.variety}`;
    const date = new Date(l.created_at);
    activities.push({
      icon,
      text: label,
      time: date.toLocaleDateString(currentLang === "ta" ? "ta-IN" : "en-GB", { day: "numeric", month: "short" })
    });
  });

  // Limit to 4 items total
  const displayed = activities.slice(0, 4);

  if (displayed.length === 0) {
    container.innerHTML = `<p class="activity-empty" data-i18n="activity_empty">${translations[currentLang].activity_empty}</p>`;
    return;
  }

  container.innerHTML = displayed.map(a => `
    <div class="activity-item">
      <span class="activity-icon" aria-hidden="true">${a.icon}</span>
      <span class="activity-text">${escapeHTML(a.text)}</span>
      <span class="activity-time">${escapeHTML(a.time)}</span>
    </div>
  `).join("");
}

// ============================================================
// HISTORY FILTER
// ============================================================
function filterHistory(filter) {
  activeHistoryFilter = filter;
  // Update button states
  ["all", "healthy", "disease", "uncertain"].forEach(f => {
    const btn = document.getElementById(`filter-${f}`);
    if (btn) btn.classList.toggle("active", f === filter);
  });
  renderHistory(getFilteredDiagnoses());
}

function getFilteredDiagnoses() {
  switch (activeHistoryFilter) {
    case "healthy":
      return cachedDiagnoses.filter(d => d.disease.toLowerCase().includes("healthy"));
    case "disease":
      return cachedDiagnoses.filter(d => !d.disease.toLowerCase().includes("healthy") && !d.is_uncertain && d.confidence >= 0.70);
    case "uncertain":
      return cachedDiagnoses.filter(d => d.is_uncertain || d.confidence < 0.70);
    default:
      return cachedDiagnoses;
  }
}

// ============================================================
// DRAG & DROP HANDLERS
// ============================================================
function handleDragOver(e) {
  e.preventDefault();
  e.stopPropagation();
  const dropZone = document.getElementById("drop-zone");
  if (dropZone) dropZone.classList.add("dragover");
}

function handleDragLeave(e) {
  e.preventDefault();
  e.stopPropagation();
  const dropZone = document.getElementById("drop-zone");
  if (dropZone) dropZone.classList.remove("dragover");
}

function handleDrop(e) {
  e.preventDefault();
  e.stopPropagation();
  const dropZone = document.getElementById("drop-zone");
  if (dropZone) dropZone.classList.remove("dragover");

  const dt = e.dataTransfer;
  const files = dt.files;
  if (files && files.length > 0) {
    const fileInput = document.getElementById("leaf-file");
    fileInput.files = files;
    onFileSelected(fileInput);
  }
}

function triggerFileSelect() {
  const fileInput = document.getElementById("leaf-file");
  if (fileInput) fileInput.click();
}

// ============================================================
// FILE SELECTION — PREVIEW
// ============================================================
function onFileSelected(input) {
  const chosenText = document.getElementById("file-chosen-text");
  const previewContainer = document.getElementById("upload-preview-container");
  const previewImg = document.getElementById("upload-preview");

  if (input.files && input.files[0]) {
    const file = input.files[0];
    if (chosenText) chosenText.textContent = file.name;
    if (previewImg) previewImg.src = URL.createObjectURL(file);
    if (previewContainer) previewContainer.classList.remove("hidden");
  } else {
    if (chosenText) chosenText.textContent = translations[currentLang].choose_image;
    if (previewContainer) previewContainer.classList.add("hidden");
  }
}

// ============================================================
// MARKETPLACE LIVE PREVIEW
// ============================================================
function updateListingPreview() {
  const variety = document.getElementById("list-variety");
  const price = document.getElementById("list-price");
  const quantity = document.getElementById("list-quantity");
  const location = document.getElementById("list-location");

  const previewVariety = document.getElementById("preview-variety");
  const previewPrice = document.getElementById("preview-price");
  const previewQty = document.getElementById("preview-qty");
  const previewLocation = document.getElementById("preview-location");

  if (previewVariety) previewVariety.textContent = (variety ? variety.value : "—") + " Cocoons";
  if (previewPrice) previewPrice.textContent = price && price.value ? `₹${price.value} / kg` : "₹— / kg";
  if (previewQty) previewQty.textContent = quantity && quantity.value ? quantity.value : "—";
  if (previewLocation) previewLocation.textContent = location && location.value ? location.value : "—";
}

// ============================================================
// DELAY HELPER
// ============================================================
const delay = ms => new Promise(res => setTimeout(res, ms));

// ============================================================
// DIAGNOSIS UPLOAD
// ============================================================
async function handleDiagnoseUpload(event) {
  event.preventDefault();

  const token = localStorage.getItem("token");
  const fileInput = document.getElementById("leaf-file");
  const variety = document.getElementById("farmer-variety").textContent;

  const resultBox = document.getElementById("diagnosis-result");
  const loadingBox = document.getElementById("loading-steps-container");
  const btnDiagnose = document.getElementById("btn-diagnose");

  if (!fileInput.files || fileInput.files.length === 0) {
    showToast("Please select a leaf photo first.", "warning");
    return;
  }

  btnDiagnose.disabled = true;
  resultBox.classList.add("hidden");

  const checks = [
    document.getElementById("check-1"),
    document.getElementById("check-2"),
    document.getElementById("check-3")
  ];
  const steps = [
    document.getElementById("step-1"),
    document.getElementById("step-2"),
    document.getElementById("step-3")
  ];

  checks.forEach(el => { if (el) el.textContent = "⚪"; });
  steps.forEach(el => { if (el) el.className = "step-item"; });

  loadingBox.classList.remove("hidden");

  // Step 1
  if (checks[0]) checks[0].textContent = "⏳";
  if (steps[0]) steps[0].className = "step-item active";
  await delay(450);
  if (checks[0]) checks[0].textContent = "✅";
  if (steps[0]) steps[0].className = "step-item done";

  // Step 2
  if (checks[1]) checks[1].textContent = "⏳";
  if (steps[1]) steps[1].className = "step-item active";
  await delay(450);
  if (checks[1]) checks[1].textContent = "✅";
  if (steps[1]) steps[1].className = "step-item done";

  // Step 3 — actual request
  if (checks[2]) checks[2].textContent = "⏳";
  if (steps[2]) steps[2].className = "step-item active";

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("variety", variety);

  try {
    const res = await fetch(`${API_BASE_URL}/api/diagnose/upload`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${token}` },
      body: formData
    });

    const data = await res.json();

    // 401 means token expired or invalid — redirect to login
    if (res.status === 401) {
      loadingBox.classList.add("hidden");
      btnDiagnose.disabled = false;
      showToast("Your session has expired. Please log in again.", "error");
      setTimeout(() => {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        showView("authView");
      }, 2000);
      return;
    }

    if (!res.ok) throw new Error(data.detail || "Leaf analysis could not be completed.");


    if (checks[2]) checks[2].textContent = "✅";
    if (steps[2]) steps[2].className = "step-item done";
    await delay(300);

    loadingBox.classList.add("hidden");
    resultBox.classList.remove("hidden");

    // Populate result
    document.getElementById("result-disease").textContent = data.disease;

    const confidencePercent = Math.round(data.confidence * 100);
    document.getElementById("result-confidence").textContent = `${confidencePercent}%`;

    const confBar = document.getElementById("result-confidence-bar");
    if (confBar) {
      confBar.style.width = "0%";
      const confBarA11y = confBar.parentElement;
      if (confBarA11y) confBarA11y.setAttribute("aria-valuenow", String(confidencePercent));
      setTimeout(() => { confBar.style.width = `${confidencePercent}%`; }, 50);
    }

    const resultAdvisory = document.getElementById("result-advisory-box");
    const resultTreatment = document.getElementById("result-treatment");
    const resultWarning = document.getElementById("result-warning");
    const askDiseaseBtn = document.getElementById("btn-ask-disease");

    if (data.is_uncertain) {
      if (resultAdvisory) resultAdvisory.classList.add("hidden");
      if (resultWarning) resultWarning.classList.remove("hidden");
      if (askDiseaseBtn) askDiseaseBtn.classList.add("hidden");
      showToast(translations[currentLang].toast_diagnosis_uncertain, "warning");
    } else {
      if (resultWarning) resultWarning.classList.add("hidden");
      if (resultAdvisory) resultAdvisory.classList.remove("hidden");
      if (resultTreatment) resultTreatment.textContent = data.advisory[currentLang] || data.advisory.en;
      const isHealthy = data.disease.toLowerCase().includes("healthy");
      if (askDiseaseBtn) askDiseaseBtn.classList.toggle("hidden", isHealthy);
      showToast(translations[currentLang].toast_diagnosis_done, "success");
    }

    // Update history cache
    cachedDiagnoses.unshift({
      id: data.id,
      user_id: data.user_id,
      disease: data.disease,
      confidence: data.confidence,
      variety: data.variety,
      timestamp: data.timestamp,
      severity: data.severity,
      is_uncertain: data.is_uncertain,
      image_path: data.image_path
    });

    renderHistory(getFilteredDiagnoses());
    renderRecentActivity();
    updateHealthScore();
    updateRecommendedAction();
    updateFarmSnapshot();

    // Reset upload form
    document.getElementById("upload-form").reset();
    document.getElementById("upload-preview-container").classList.add("hidden");
    document.getElementById("file-chosen-text").textContent = translations[currentLang].choose_image;

  } catch (err) {
    loadingBox.classList.add("hidden");
    if (checks[2]) checks[2].textContent = "❌";
    showToast(err.message || "We couldn't complete the diagnosis. Please try again.", "error");
  } finally {
    btnDiagnose.disabled = false;
  }
}

// ============================================================
// SIGN UP
// ============================================================
async function handleSignup(event) {
  event.preventDefault();
  const errorEl = document.getElementById("signup-error");
  errorEl.textContent = "";

  const name = document.getElementById("signup-name").value;
  const email = document.getElementById("signup-email").value || null;
  const phone = document.getElementById("signup-phone").value || null;
  const village = document.getElementById("signup-village").value;
  const password = document.getElementById("signup-password").value;
  const variety = document.getElementById("signup-variety").value;
  const language = document.getElementById("signup-language").value;

  if (!email && !phone) {
    errorEl.textContent = "Please provide either an email or phone number.";
    return;
  }

  try {
    const res = await fetch(`${API_BASE_URL}/api/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, phone, password, role: "farmer", preferred_language: language, village })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Registration failed. Please check your details.");

    localStorage.setItem("token", data.access_token);
    data.user.preferred_variety = variety;
    localStorage.setItem("user", JSON.stringify(data.user));

    updateAuthUI();
  } catch (err) {
    errorEl.textContent = err.message;
  }
}

// ============================================================
// LOGIN
// ============================================================
async function handleLogin(event) {
  event.preventDefault();
  const errorEl = document.getElementById("login-error");
  errorEl.textContent = "";

  const identifier = document.getElementById("login-identifier").value;
  const password = document.getElementById("login-password").value;
  const btn = document.getElementById("btn-login");
  if (btn) { btn.disabled = true; btn.textContent = "Logging in..."; }

  try {
    const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ identifier, password })
    });

    const data = await res.json();
    if (!res.ok) throw new Error("Invalid email/phone or password.");

    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));

    updateAuthUI();
  } catch (err) {
    errorEl.textContent = err.message;
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = translations[currentLang].btn_login;
    }
  }
}

// ============================================================
// WEATHER RISK
// ============================================================
async function loadWeatherRisk() {
  const token = localStorage.getItem("token");
  const riskList = document.getElementById("risk-alert-list");

  try {
    const res = await fetch(`${API_BASE_URL}/api/weather/risk`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (!res.ok) throw new Error("Failed to load weather data");

    const data = await res.json();
    cachedWeatherRisk = data;
    renderWeatherRisk(cachedWeatherRisk);
    updateHealthScore();
    updateRecommendedAction();
  } catch (err) {
    if (riskList) riskList.innerHTML = `<p class="error-msg">Failed to load weather advisory.</p>`;
  }
}

function renderWeatherRisk(data) {
  if (!data) return;

  const tempEl = document.getElementById("weather-val-temp");
  const humEl = document.getElementById("weather-val-humidity");
  const condEl = document.getElementById("weather-val-condition");
  if (tempEl) tempEl.textContent = `${data.weather.temp}°C`;
  if (humEl) humEl.textContent = `${data.weather.humidity}%`;
  if (condEl) condEl.textContent = data.weather.condition[currentLang] || data.weather.condition.en;

  const riskList = document.getElementById("risk-alert-list");
  if (!riskList) return;
  riskList.innerHTML = "";

  data.risks.forEach(item => {
    const diseaseName = currentLang === "ta" ? item.disease_ta : item.disease;
    const reasonText = item.reason[currentLang] || item.reason.en;
    const disclaimerText = item.disclaimer[currentLang] || item.disclaimer.en;
    const levelLower = item.risk_level.toLowerCase();

    let riskLabel = "";
    if (item.risk_level === "High") riskLabel = translations[currentLang].risk_label_high;
    else if (item.risk_level === "Moderate") riskLabel = translations[currentLang].risk_label_moderate;
    else riskLabel = translations[currentLang].risk_label_low;

    const dotMap = { high: "🔴", moderate: "🟠", low: "🟢" };
    const dot = dotMap[levelLower] || "⚪";

    riskList.insertAdjacentHTML("beforeend", `
      <div class="risk-card risk-${escapeHTML(levelLower)}" role="article">
        <div class="risk-card-header">
          <span class="risk-disease">${dot} ${escapeHTML(diseaseName)}</span>
          <span class="risk-badge badge-${escapeHTML(levelLower)}">${escapeHTML(riskLabel)}</span>
        </div>
        <p class="risk-reason">${escapeHTML(reasonText)}</p>
        <p class="risk-disclaimer">⚠ ${escapeHTML(disclaimerText)}</p>
      </div>
    `);
  });

  updateFarmSnapshot();
}

// ============================================================
// CHATBOT
// ============================================================
function appendChatMessage(sender, text) {
  const transcript = document.getElementById("chat-transcript");
  if (!transcript) return;

  const msgDiv = document.createElement("div");
  msgDiv.className = `chat-msg ${sender === "user" ? "msg-user" : "msg-assistant"}`;

  const avatarDiv = document.createElement("div");
  avatarDiv.className = "msg-avatar";
  avatarDiv.setAttribute("aria-hidden", "true");
  avatarDiv.textContent = sender === "user" ? "👤" : "🌿";

  const bubbleDiv = document.createElement("div");
  bubbleDiv.className = "msg-bubble";

  const p = document.createElement("p");
  const lines = text.split("\n");
  lines.forEach((line, index) => {
    p.appendChild(document.createTextNode(line));
    if (index < lines.length - 1) p.appendChild(document.createElement("br"));
  });

  bubbleDiv.appendChild(p);
  msgDiv.appendChild(avatarDiv);
  msgDiv.appendChild(bubbleDiv);
  transcript.appendChild(msgDiv);
  transcript.scrollTop = transcript.scrollHeight;
}

async function handleChatSubmit(event) {
  if (event) event.preventDefault();

  const inputEl = document.getElementById("chat-input");
  const queryText = inputEl.value.trim();
  if (!queryText) return;

  inputEl.value = "";
  appendChatMessage("user", queryText);

  // Maintain short-term chat session memory
  chatSessionHistory.push({ role: "user", content: queryText });

  const typingIndicator = document.getElementById("chat-typing-indicator");
  if (typingIndicator) typingIndicator.classList.remove("hidden");

  const token = localStorage.getItem("token");

  try {
    const payload = {
      message: queryText,
      language: currentLang,
      diagnosis_context: activeDiagnosisContext,
      session_history: chatSessionHistory.slice(-6)
    };

    const res = await fetch(`${API_BASE_URL}/api/chat/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (typingIndicator) typingIndicator.classList.add("hidden");

    if (!res.ok) throw new Error(data.detail || "Chat service failed.");
    
    appendChatMessage("assistant", data.reply);
    chatSessionHistory.push({ role: "assistant", content: data.reply });

    // If context was returned or updated, sync with banner
    if (data.diagnosis_context && !activeDiagnosisContext) {
      activeDiagnosisContext = data.diagnosis_context;
      updateChatDiagnosisBanner();
    }
  } catch (err) {
    if (typingIndicator) typingIndicator.classList.add("hidden");
    appendChatMessage("assistant", translations[currentLang].chat_err);
  }
}

function updateChatDiagnosisBanner() {
  const banner = document.getElementById("chat-diagnosis-banner");
  const disEl = document.getElementById("chat-context-disease");
  const confEl = document.getElementById("chat-context-conf");
  if (!banner || !disEl) return;

  if (activeDiagnosisContext && activeDiagnosisContext.disease) {
    disEl.textContent = activeDiagnosisContext.disease;
    if (confEl) {
      const confVal = activeDiagnosisContext.confidence ? `${activeDiagnosisContext.confidence}%` : "";
      confEl.textContent = confVal;
      confEl.style.display = confVal ? "inline-block" : "none";
    }
    banner.classList.remove("hidden");
  } else {
    banner.classList.add("hidden");
  }
}

function clearChatDiagnosisContext() {
  activeDiagnosisContext = null;
  updateChatDiagnosisBanner();
  showToast(currentLang === "ta" ? "நோய் சூழல் நீக்கப்பட்டது" : "Diagnosis context cleared", "info");
}

function sendQuickAction(actionKey) {
  if (actionKey === "check_leaf") {
    switchDashboardView("diagnose");
    return;
  }

  const actions = {
    en: {
      today_checklist: "What should I do today on my farm?",
      leaves_unhealthy: "My mulberry leaves look unhealthy. What should I check?",
      when_irrigate: "When and how often should I irrigate my mulberry garden?",
      found_pests: "I found pests on my mulberry leaves. How should I control them?",
      how_prune: "How and when should I prune my mulberry plants?",
      worms_sick: "My silkworms look sick. What symptoms should I check?",
      prepare_cocoons: "How do I prepare harvested cocoons for sale in the market?"
    },
    ta: {
      today_checklist: "இன்று என் பண்ணையில் என்ன செய்ய வேண்டும்?",
      leaves_unhealthy: "என் மல்பெரி இலைகள் ஆரோக்கியமற்றதாக தெரிகின்றன. நான் என்ன கவனிக்க வேண்டும்?",
      when_irrigate: "மல்பெரி தோட்டத்திற்கு எப்போது, எவ்வளவு தண்ணீர் பாய்ச்ச வேண்டும்?",
      found_pests: "என் மல்பெரி இலைகளில் பூச்சிகள் தென்படுகின்றன. அவற்றை எவ்வாறு கட்டுப்படுத்துவது?",
      how_prune: "மல்பெரி செடிகளை எவ்வாறு மற்றும் எப்போது கவாத்து செய்ய வேண்டும்?",
      worms_sick: "என் பட்டுப்புழுக்கள் நோய்வாய்ப்பட்டுள்ளன. நான் என்ன செய்ய வேண்டும்?",
      prepare_cocoons: "அறுவடை செய்யப்பட்ட பட்டுக்கூடுகளை விற்பனைக்கு எவ்வாறு தயார் செய்வது?"
    }
  };

  const prompt = (actions[currentLang] && actions[currentLang][actionKey]) || (actions.en && actions.en[actionKey]) || "";
  if (!prompt) return;

  const inputEl = document.getElementById("chat-input");
  if (inputEl) {
    inputEl.value = prompt;
    handleChatSubmit();
  }
}

function sendSuggestedQuestion(topic) {
  const inputEl = document.getElementById("chat-input");
  let question = "";

  const questions = {
    en: {
      pruning: "How should I prune mulberry plants?",
      irrigation: "How often should I water mulberry?",
      disease: "What are common leaf diseases in mulberry?",
      fertilizer: "What is the recommended NPK fertilizer dosage?",
      silkworm: "How to rear silkworms and disinfect rearing beds?",
      selling: "Where and how can I sell cocoons?"
    },
    ta: {
      pruning: "மல்பெரி செடிகளை எவ்வாறு கவாத்து செய்ய வேண்டும்?",
      irrigation: "மல்பெரிக்கு எவ்வளவு தண்ணீர் பாய்ச்ச வேண்டும்?",
      disease: "மல்பெரியில் ஏற்படும் பொதுவான இலை நோய்கள் யாவை?",
      fertilizer: "பரிந்துரைக்கப்பட்ட உர அளவு (NPK) என்ன?",
      silkworm: "பட்டுப்புழுக்களை எவ்வாறு வளர்ப்பது மற்றும் படுக்கைகளை சுத்தம் செய்வது?",
      selling: "பட்டுக்கூடுகளை எங்கு மற்றும் எவ்வாறு விற்பனை செய்வது?"
    }
  };

  question = (questions[currentLang] && questions[currentLang][topic]) || (questions.en[topic] || "");
  inputEl.value = question;
  handleChatSubmit();
}

function askAboutCurrentDisease() {
  const diseaseEl = document.getElementById("result-disease");
  const diseaseName = diseaseEl ? diseaseEl.textContent.trim() : "Leaf Rust";
  const confEl = document.getElementById("result-confidence");
  const confText = confEl ? confEl.textContent.replace("%", "").trim() : "85";
  const confVal = parseInt(confText) || 85;

  const varietyEl = document.getElementById("snapshot-val-variety");
  const variety = varietyEl ? varietyEl.textContent.trim() : "S36";

  // Set active diagnosis context for chat
  activeDiagnosisContext = {
    disease: diseaseName,
    confidence: confVal,
    variety: variety
  };

  updateChatDiagnosisBanner();
  switchDashboardView("chat");

  const inputEl = document.getElementById("chat-input");
  const question = currentLang === "ta"
    ? `மல்பெரியில் உள்ள ${diseaseName} நோய் பற்றி எனக்குக் கூறுங்கள்.`
    : `Tell me more about ${diseaseName} in mulberry.`;

  inputEl.value = question;
  setTimeout(() => handleChatSubmit(), 300);
}

// ============================================================
// MARKETPLACE
// ============================================================
function switchMarketTab(tab) {
  const findTab = document.getElementById("tab-find-cocoons");
  const sellTab = document.getElementById("tab-sell-cocoons");
  const findView = document.getElementById("view-find-cocoons");
  const sellView = document.getElementById("view-sell-cocoons");

  if (tab === "find") {
    if (findTab) { findTab.classList.add("active"); findTab.setAttribute("aria-selected", "true"); }
    if (sellTab) { sellTab.classList.remove("active"); sellTab.setAttribute("aria-selected", "false"); }
    if (findView) findView.classList.remove("hidden");
    if (sellView) sellView.classList.add("hidden");
    searchMarketListings();
  } else {
    if (sellTab) { sellTab.classList.add("active"); sellTab.setAttribute("aria-selected", "true"); }
    if (findTab) { findTab.classList.remove("active"); findTab.setAttribute("aria-selected", "false"); }
    if (sellView) sellView.classList.remove("hidden");
    if (findView) findView.classList.add("hidden");
    loadMyListings();
    updateListingPreview();
  }
}

async function handleCreateListing(event) {
  event.preventDefault();

  const successEl = document.getElementById("listing-form-success");
  const errorEl = document.getElementById("listing-form-error");
  if (successEl) successEl.classList.add("hidden");
  if (errorEl) errorEl.textContent = "";

  const token = localStorage.getItem("token");
  const variety = document.getElementById("list-variety").value;
  const price = parseFloat(document.getElementById("list-price").value);
  const quantity = parseFloat(document.getElementById("list-quantity").value);
  const locationName = document.getElementById("list-location").value;
  const phone = document.getElementById("list-phone").value;
  const desc = document.getElementById("list-desc").value || null;

  // Frontend validation
  if (!variety || isNaN(price) || price <= 0) {
    if (errorEl) errorEl.textContent = "Please enter a valid price.";
    return;
  }
  if (isNaN(quantity) || quantity <= 0) {
    if (errorEl) errorEl.textContent = "Please enter a valid quantity.";
    return;
  }
  if (!locationName.trim()) {
    if (errorEl) errorEl.textContent = "Please enter a location.";
    return;
  }
  if (!phone.trim()) {
    if (errorEl) errorEl.textContent = "Please enter a contact phone number.";
    return;
  }

  try {
    const res = await fetch(`${API_BASE_URL}/api/listings/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        variety, price_per_kg: price, quantity_kg: quantity,
        location: locationName, contact_phone: phone, description: desc
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || translations[currentLang].list_err);

    if (successEl) {
      successEl.textContent = translations[currentLang].list_success;
      successEl.classList.remove("hidden");
    }
    showToast(translations[currentLang].toast_listing_published, "success");

    // Clear price/qty/desc fields only
    document.getElementById("list-price").value = "";
    document.getElementById("list-quantity").value = "";
    document.getElementById("list-desc").value = "";

    loadMyListings();
    updateListingPreview();

    setTimeout(() => {
      if (successEl) successEl.classList.add("hidden");
    }, 4000);
  } catch (err) {
    if (errorEl) errorEl.textContent = err.message;
  }
}

async function searchMarketListings() {
  const token = localStorage.getItem("token");
  const resultsBox = document.getElementById("market-search-results");
  const locationFilter = document.getElementById("search-location").value;
  const varietyFilter = document.getElementById("search-variety").value;

  let query = "";
  if (locationFilter && locationFilter.trim()) query += `&location=${encodeURIComponent(locationFilter.trim())}`;
  if (varietyFilter) query += `&variety=${encodeURIComponent(varietyFilter)}`;

  try {
    if (resultsBox) resultsBox.innerHTML = `<p class="loading-msg">${translations[currentLang].connecting}</p>`;

    const res = await fetch(`${API_BASE_URL}/api/listings/search?_t=1${query}`, {
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (!res.ok) throw new Error("Search request failed.");

    const listings = await res.json();
    cachedMarketListings = listings;
    renderMarketListings(cachedMarketListings);
  } catch (err) {
    if (resultsBox) resultsBox.innerHTML = `<p class="error-msg">Search error. Please check your connection and try again.</p>`;
  }
}

function renderMarketListings(listings) {
  const resultsBox = document.getElementById("market-search-results");
  if (!resultsBox) return;

  if (!listings || listings.length === 0) {
    resultsBox.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">🧺</div>
        <p class="empty-state-title" data-i18n="marketplace_empty_title">${translations[currentLang].marketplace_empty_title}</p>
        <p class="empty-state-desc" data-i18n="marketplace_empty_desc">${translations[currentLang].marketplace_empty_desc}</p>
        <button class="btn btn-secondary empty-state-btn" onclick="document.getElementById('search-location').value='';document.getElementById('search-variety').value='';searchMarketListings()">Clear Filters</button>
      </div>
    `;
    return;
  }

  resultsBox.innerHTML = "";
  listings.forEach(item => {
    const date = new Date(item.created_at);
    const formattedDate = date.toLocaleDateString(currentLang === "ta" ? "ta-IN" : "en-GB", {
      day: "numeric", month: "short", year: "numeric"
    });

    resultsBox.insertAdjacentHTML("beforeend", `
      <div class="listing-card-market" id="market-card-${escapeHTML(String(item.id))}">
        <div class="listing-card-header">
          <span class="listing-title">🐛 ${escapeHTML(item.variety)} Cocoons</span>
          <span class="price-tag">₹${escapeHTML(String(item.price_per_kg))} / kg</span>
        </div>
        <div class="listing-details-grid">
          <div class="listing-detail-item">
            <span aria-hidden="true">📦</span>
            <span>${translations[currentLang].label_list_quantity}: <strong>${escapeHTML(String(item.quantity_kg))} kg</strong></span>
          </div>
          <div class="listing-detail-item">
            <span aria-hidden="true">📍</span>
            <span>${translations[currentLang].label_list_location}: <strong>${escapeHTML(item.location)}</strong></span>
          </div>
        </div>
        ${item.description ? `<p class="listing-desc">${escapeHTML(item.description)}</p>` : ""}
        <div class="listing-footer">
          <span class="self-reported-badge">${translations[currentLang].self_reported}</span>
          <span class="listing-date">${translations[currentLang].listed_on}: ${formattedDate}</span>
        </div>
        <button class="btn btn-secondary btn-contact"
                onclick="revealContactPhone('${escapeHTML(String(item.id))}', '${escapeHTML(item.contact_phone)}')"
                style="margin-top:10px;width:100%">
          📞 ${translations[currentLang].contact_seller}
        </button>
        <div id="contact-reveal-${escapeHTML(String(item.id))}" class="contact-expanded-box hidden"></div>
      </div>
    `);
  });
}

function revealContactPhone(listingId, phoneNum) {
  const box = document.getElementById(`contact-reveal-${listingId}`);
  if (!box) return;
  if (box.classList.contains("hidden")) {
    box.innerHTML = `
      <span>📞 ${translations[currentLang].contact_prefix}:</span>
      <a href="tel:${escapeHTML(phoneNum)}" style="margin-left:6px;font-weight:800">${escapeHTML(phoneNum)}</a>
    `;
    box.classList.remove("hidden");
  } else {
    box.classList.add("hidden");
  }
}

async function loadMyListings() {
  const token = localStorage.getItem("token");
  try {
    const res = await fetch(`${API_BASE_URL}/api/listings/my`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (!res.ok) throw new Error("Unable to retrieve listings.");

    const myListings = await res.json();
    cachedMyListings = myListings;
    renderMyListings(cachedMyListings);
    renderRecentActivity();
  } catch (err) {
    console.error("Personal listings error:", err);
  }
}

function renderMyListings(listings) {
  const listEl = document.getElementById("my-listings-list");
  if (!listEl) return;

  if (!listings || listings.length === 0) {
    listEl.innerHTML = `<p class="empty-msg">${currentLang === "ta" ? "பட்டியல்கள் இல்லை." : "No active listings found."}</p>`;
    return;
  }

  listEl.innerHTML = "";
  listings.forEach(item => {
    const isSold = item.status === "sold";
    listEl.insertAdjacentHTML("beforeend", `
      <div class="my-listing-row">
        <div class="my-listing-info">
          <span class="my-listing-title">🐛 ${escapeHTML(item.variety)} (${escapeHTML(String(item.quantity_kg))} kg)</span>
          <span class="my-listing-meta">₹${escapeHTML(String(item.price_per_kg))}/kg @ ${escapeHTML(item.location)}</span>
        </div>
        <div class="my-listing-actions">
          <span class="status-tag status-${escapeHTML(item.status)}">
            ${item.status === "active" ? translations[currentLang].btn_active : translations[currentLang].btn_sold}
          </span>
          ${!isSold ? `
            <button class="btn btn-secondary btn-sold-action"
                    onclick="toggleMarkAsSold('${escapeHTML(String(item.id))}')">
              ✅ ${translations[currentLang].btn_mark_sold}
            </button>
          ` : ""}
        </div>
      </div>
    `);
  });
}

async function toggleMarkAsSold(listingId) {
  const token = localStorage.getItem("token");
  try {
    const res = await fetch(`${API_BASE_URL}/api/listings/${listingId}/sold`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (!res.ok) throw new Error("Failed to update listing status.");

    showToast(translations[currentLang].toast_marked_sold, "success");
    loadMyListings();
  } catch (err) {
    showToast(err.message, "error");
  }
}

// ============================================================
// HISTORY
// ============================================================
async function loadHistory() {
  const historyList = document.getElementById("history-list");
  const token = localStorage.getItem("token");

  try {
    const res = await fetch(`${API_BASE_URL}/api/diagnose/history`, {
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (!res.ok) {
      if (res.status === 401) { handleLogout(); return; }
      throw new Error("Failed to load history");
    }

    const diagnoses = await res.json();
    cachedDiagnoses = diagnoses;
    renderHistory(getFilteredDiagnoses());
    renderRecentActivity();
    updateHealthScore();
    updateRecommendedAction();
    updateFarmSnapshot();
  } catch (err) {
    if (historyList) historyList.innerHTML = `<p class="error-msg">${translations[currentLang].load_error}</p>`;
  }
}

function renderHistory(diagnoses) {
  const historyList = document.getElementById("history-list");
  if (!historyList) return;

  const token = localStorage.getItem("token");
  if (!token) return;

  if (!diagnoses || diagnoses.length === 0) {
    const isFiltered = activeHistoryFilter !== "all";
    if (isFiltered) {
      historyList.innerHTML = `<p class="empty-msg">${translations[currentLang].no_records}</p>`;
    } else {
      historyList.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">🍃</div>
          <p class="empty-state-title">${translations[currentLang].history_empty_title}</p>
          <p class="empty-state-desc">${translations[currentLang].history_empty_desc}</p>
          <button class="btn btn-primary empty-state-btn" onclick="switchDashboardView('diagnose')">
            ${translations[currentLang].btn_diagnose}
          </button>
        </div>
      `;
    }
    return;
  }

  historyList.innerHTML = "";
  diagnoses.forEach(item => {
    const date = new Date(item.timestamp);
    const formattedDate = date.toLocaleDateString(currentLang === "ta" ? "ta-IN" : "en-GB", {
      day: "numeric", month: "short", year: "numeric"
    });

    const isHealthy = item.disease.toLowerCase().includes("healthy");
    const isUncertain = item.is_uncertain || item.confidence < 0.70;
    const confidencePercent = Math.round(item.confidence * 100);

    let cardClass = "history-card";
    if (isUncertain) cardClass += " uncertain";
    else if (isHealthy) cardClass += " healthy";
    else cardClass += " diseased";

    let html = `<div class="${cardClass}"><div class="card-content-wrapper">`;

    if (item.image_path) {
      const secureImgUrl = `${API_BASE_URL}${item.image_path}?token=${encodeURIComponent(token)}`;
      html += `
        <div class="card-preview">
          <img src="${secureImgUrl}" class="card-thumbnail" alt="Leaf Diagnosis" onerror="this.style.display='none'" />
        </div>
      `;
    }

    html += `
      <div class="card-details">
        <div class="disease-row">
          <span class="disease-name">🌿 ${escapeHTML(item.disease)}</span>
          <span class="confidence-badge">${translations[currentLang].confidence_badge}: ${confidencePercent}%</span>
        </div>
        <div class="variety-row">
          ${translations[currentLang].variety_label}: <strong>${escapeHTML(item.variety)}</strong>
        </div>
        <div class="timestamp-row">${formattedDate}</div>
    `;

    if (item.severity) {
      html += `<div><span class="severity-badge severity-${escapeHTML(item.severity.toLowerCase())}">${escapeHTML(item.severity)} ${translations[currentLang].severity_badge}</span></div>`;
    }

    if (isUncertain) {
      html += `<div class="uncertain-warning" style="margin-top:8px;font-size:0.82rem;padding:10px 12px">⚠ ${escapeHTML(translations[currentLang].uncertain_warning)}</div>`;
    }

    html += `</div></div></div>`;
    historyList.insertAdjacentHTML("beforeend", html);
  });

  updateFarmSnapshot();
}

// ============================================================
// LOGOUT
// ============================================================
function handleLogout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  cachedDiagnoses = [];
  cachedWeatherRisk = null;
  cachedMarketListings = [];
  cachedMyListings = [];
  activeHistoryFilter = "all";
  updateAuthUI();
}

// ============================================================
// INIT — DOMContentLoaded
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  checkHealth();
  updateAuthUI();
});
