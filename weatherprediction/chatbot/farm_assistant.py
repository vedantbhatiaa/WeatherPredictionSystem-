# chatbot/farm_assistant.py

class FarmAssistant:
    def __init__(self):
        # Knowledge base for crops
        self.crops_database = {
            "wheat": {
                "soil_type": ["loamy", "clay loam"],
                "climate": ["temperate", "subtropical"],
                "water_needs": "moderate",
                "growing_season": "winter",
                "ph_range": [6.0, 7.5],
                "benefits": "Good source of carbohydrates and essential minerals",
                "soil_preparation": "Prepare a fine seedbed with good drainage. Add organic matter if soil is poor."
            },
            "rice": {
                "soil_type": ["clay", "clay loam"],
                "climate": ["tropical", "subtropical"],
                "water_needs": "high",
                "growing_season": "summer",
                "ph_range": [5.5, 6.5],
                "benefits": "Staple food with good energy content",
                "soil_preparation": "Puddle the soil and level it. Maintain standing water during growing period."
            },
            "corn": {
                "soil_type": ["loamy", "sandy loam"],
                "climate": ["warm", "temperate"],
                "water_needs": "moderate",
                "growing_season": "summer",
                "ph_range": [5.8, 7.0],
                "benefits": "Versatile crop with high energy content",
                "soil_preparation": "Deep plowing followed by thorough disking. Apply nitrogen-rich fertilizers."
            },
            "tomato": {
                "soil_type": ["loamy", "sandy loam"],
                "climate": ["warm", "temperate"],
                "water_needs": "moderate",
                "growing_season": "summer",
                "ph_range": [6.0, 6.8],
                "benefits": "Rich in vitamins A and C",
                "soil_preparation": "Well-drained soil with organic matter. Avoid waterlogging."
            },
            "potato": {
                "soil_type": ["loamy", "sandy loam"],
                "climate": ["cool", "temperate"],
                "water_needs": "moderate",
                "growing_season": "spring",
                "ph_range": [5.0, 6.5],
                "benefits": "Good source of carbohydrates and vitamin C",
                "soil_preparation": "Loose, well-drained soil. Avoid compacted soils."
            }
            # Add more crops as needed
        }
        
        # Knowledge base for soil improvement
        self.soil_improvement = {
            "clay": {
                "challenges": "Poor drainage, compacts easily, slow to warm in spring",
                "improvements": [
                    "Add organic matter like compost to improve structure",
                    "Add coarse sand to improve drainage",
                    "Avoid working when wet to prevent compaction",
                    "Consider raised beds for better drainage"
                ]
            },
            "sandy": {
                "challenges": "Drains too quickly, low nutrient retention, dries out fast",
                "improvements": [
                    "Add organic matter to improve water retention",
                    "Use mulch to reduce evaporation",
                    "Consider more frequent, light watering",
                    "Add clay or silt to improve nutrient retention"
                ]
            },
            "loamy": {
                "challenges": "Generally good soil, but may still need improvements",
                "improvements": [
                    "Regular addition of compost to maintain structure",
                    "Crop rotation to prevent nutrient depletion",
                    "Cover cropping during fallow periods"
                ]
            },
            "acidic": {
                "challenges": "pH too low for many crops",
                "improvements": [
                    "Add agricultural lime to raise pH",
                    "Use dolomite lime if magnesium is also low",
                    "Avoid aluminum-containing fertilizers"
                ]
            },
            "alkaline": {
                "challenges": "pH too high for many crops",
                "improvements": [
                    "Add sulfur to lower pH",
                    "Use acidic organic materials like pine needles",
                    "Choose acid-tolerant crops if pH is difficult to adjust"
                ]
            }
            # Add more soil types as needed
        }
        
        # Common questions and answers
        self.faqs = {
            "how to start farming": "Starting farming requires planning: 1) Assess your land and resources, 2) Choose suitable crops for your climate and soil, 3) Prepare soil properly, 4) Obtain quality seeds, 5) Plan irrigation, 6) Learn about pest management, 7) Consider starting small and expanding gradually.",
            "organic farming": "Organic farming avoids synthetic fertilizers and pesticides. Key practices include: composting, crop rotation, biological pest control, cover cropping, and natural fertilizers like manure.",
            "sustainable farming": "Sustainable farming focuses on long-term soil health and environmental balance. Practices include: minimal tillage, water conservation, integrated pest management, crop diversity, and reducing chemical inputs.",
            "pest control": "Integrated Pest Management (IPM) combines biological control (beneficial insects), cultural practices (crop rotation), mechanical controls (traps), and limited chemical use as a last resort.",
            "crop rotation": "Crop rotation means changing what you plant in a specific area each season. Benefits include better pest control, improved soil fertility, and reduced soil erosion."
        }
    
    def process_query(self, user_input):
        """Process the user's query and return appropriate response"""
        user_input = user_input.lower()
        
        # Check if it's a crop recommendation query
        if "which crop" in user_input or "best crop" in user_input or "recommend crop" in user_input:
            return self._recommend_crop(user_input)
        
        # Check if it's a soil improvement query
        elif "improve soil" in user_input or "soil health" in user_input or "better soil" in user_input:
            return self._soil_improvement_advice(user_input)
        
        # Check if it's about a specific crop
        elif any(crop in user_input for crop in self.crops_database.keys()):
            for crop in self.crops_database.keys():
                if crop in user_input:
                    return self._crop_information(crop, user_input)
        
        # Check for FAQs
        elif any(keyword in user_input for keyword in self.faqs.keys()):
            for keyword in self.faqs.keys():
                if keyword in user_input:
                    return self.faqs[keyword]
        
        # General greeting
        elif any(greeting in user_input for greeting in ["hello", "hi", "greetings", "hey"]):
            return "Hello! I'm your farming assistant. I can help you with crop recommendations, soil improvement, and farming practices. What would you like to know about?"
        
        # Help message for unrecognized queries
        else:
            return "I can help you with crop recommendations, soil improvement tips, and information about specific crops. Try asking something like:\n- Which crop is best for sandy soil?\n- How can I improve clay soil?\n- Tell me about growing rice\n- How to start farming"
    
    def _recommend_crop(self, query):
        """Recommend crops based on user's conditions"""
        response = "Based on the information you provided, "
        
        # Check for soil type mentions
        soil_types = {
            "sandy": ["sandy", "sand"],
            "clay": ["clay"],
            "loamy": ["loam", "loamy"],
            "silty": ["silt", "silty"]
        }
        
        detected_soil = None
        for soil, keywords in soil_types.items():
            if any(keyword in query for keyword in keywords):
                detected_soil = soil
                break
        
        # Check for climate mentions
        climates = {
            "tropical": ["tropical", "hot and humid"],
            "temperate": ["temperate", "mild"],
            "cool": ["cool", "cold"],
            "warm": ["warm", "hot"]
        }
        
        detected_climate = None
        for climate, keywords in climates.items():
            if any(keyword in query for keyword in keywords):
                detected_climate = climate
                break
        
        # Build recommendation based on detected conditions
        suitable_crops = []
        
        for crop, data in self.crops_database.items():
            matches = 0
            total_factors = 0
            
            if detected_soil:
                total_factors += 1
                if any(soil_type.startswith(detected_soil) for soil_type in data["soil_type"]):
                    matches += 1
            
            if detected_climate:
                total_factors += 1
                if detected_climate in data["climate"]:
                    matches += 1
            
            # Add more factors here as needed
            
            # If no specific factors were mentioned or all mentioned factors match
            if total_factors == 0 or (total_factors > 0 and matches == total_factors):
                suitable_crops.append(crop)
        
        if suitable_crops:
            response += f"these crops may be suitable: {', '.join(suitable_crops)}.\n\n"
            response += "Would you like specific information about any of these crops?"
        else:
            response = "I need more information to recommend crops. Could you tell me about your soil type (sandy, clay, loamy) and climate conditions (tropical, temperate, cool, warm)?"
        
        return response
    
    def _soil_improvement_advice(self, query):
        """Provide soil improvement advice"""
        # Check for soil type mentions
        soil_types = {
            "sandy": ["sandy", "sand"],
            "clay": ["clay"],
            "loamy": ["loam", "loamy"],
            "acidic": ["acidic", "low ph"],
            "alkaline": ["alkaline", "high ph"]
        }
        
        detected_soil = None
        for soil, keywords in soil_types.items():
            if any(keyword in query for keyword in keywords):
                detected_soil = soil
                break
        
        if detected_soil and detected_soil in self.soil_improvement:
            soil_data = self.soil_improvement[detected_soil]
            response = f"For {detected_soil} soil:\n\nChallenges: {soil_data['challenges']}\n\nImprovement techniques:\n"
            for i, technique in enumerate(soil_data["improvements"], 1):
                response += f"{i}. {technique}\n"
            return response
        else:
            return "To give specific soil improvement advice, I need to know your soil type. Is it sandy, clay, loamy, acidic, or alkaline? You can also get your soil tested for more accurate information."
    
    def _crop_information(self, crop, query):
        """Provide information about a specific crop"""
        crop_data = self.crops_database[crop]
        
        # Check if query is about a specific aspect of the crop
        aspects = {
            "soil": ["soil", "ground", "dirt"],
            "climate": ["climate", "weather", "temperature"],
            "water": ["water", "irrigation", "moisture"],
            "season": ["season", "time", "when to plant"],
            "benefits": ["benefit", "nutrition", "health"],
            "preparation": ["preparation", "prepare", "ready"]
        }
        
        for aspect, keywords in aspects.items():
            if any(keyword in query for keyword in keywords):
                if aspect == "soil":
                    return f"{crop.capitalize()} grows best in {', '.join(crop_data['soil_type'])} soil with a pH range of {crop_data['ph_range'][0]} to {crop_data['ph_range'][1]}.\n\nSoil preparation: {crop_data['soil_preparation']}"
                elif aspect == "climate":
                    return f"{crop.capitalize()} thrives in {', '.join(crop_data['climate'])} climates."
                elif aspect == "water":
                    return f"{crop.capitalize()} has {crop_data['water_needs']} water needs."
                elif aspect == "season":
                    return f"{crop.capitalize()} is typically grown in the {crop_data['growing_season']} season."
                elif aspect == "benefits":
                    return f"Benefits of {crop}: {crop_data['benefits']}"
                elif aspect == "preparation":
                    return f"Soil preparation for {crop}: {crop_data['soil_preparation']}"
        
        # If no specific aspect is mentioned, provide general information
        response = f"Information about {crop.capitalize()}:\n\n"
        response += f"• Best soil types: {', '.join(crop_data['soil_type'])}\n"
        response += f"• Suitable climate: {', '.join(crop_data['climate'])}\n"
        response += f"• Water needs: {crop_data['water_needs']}\n"
        response += f"• Growing season: {crop_data['growing_season']}\n"
        response += f"• Soil pH range: {crop_data['ph_range'][0]} to {crop_data['ph_range'][1]}\n"
        response += f"• Benefits: {crop_data['benefits']}\n"
        response += f"• Soil preparation: {crop_data['soil_preparation']}\n"
        
        return response