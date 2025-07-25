import json
import re
from typing import List, Dict

class GutHealthDatasetGenerator:
    def __init__(self, text_file_path: str):
        """Initialize with the scraped text file"""
        with open(text_file_path, encoding='utf-8') as f:
            self.text = f.read().lower()
        
        self.qas = []
        self.processed_topics = set()
    
    def extract_symptoms_info(self) -> None:
        """Extract information about gut health symptoms"""
        symptom_keywords = ['bloating', 'gas', 'constipation', 'diarrhea', 'cramping', 
                           'abdominal pain', 'nausea', 'heartburn', 'acid reflux']
        
        found_symptoms = [symptom for symptom in symptom_keywords if symptom in self.text]
        
        if found_symptoms and 'symptoms' not in self.processed_topics:
            self.qas.append({
                "instruction": "What are the common symptoms of an unhealthy gut?",
                "response": f"Common signs of an unhealthy gut include {', '.join(found_symptoms[:3])}, and other digestive issues. These symptoms often indicate an imbalance in your gut microbiome and may be accompanied by fatigue, brain fog, or mood changes. Your body is signaling that your digestive system needs attention."
            })
            
            self.qas.append({
                "instruction": "I've been experiencing bloating and gas. What could this mean?",
                "response": "Bloating and gas are very common gut health issues that many people experience. They can be caused by several factors including food intolerances, eating too quickly, stress, or an imbalance in gut bacteria. Try keeping a food diary, eating more slowly, and consider adding probiotics to your routine. If symptoms persist, it's worth discussing with a healthcare provider."
            })
            
            self.processed_topics.add('symptoms')
    
    def extract_probiotics_info(self) -> None:
        """Extract information about probiotics"""
        probiotic_indicators = ['probiotics', 'beneficial bacteria', 'good bacteria', 'lactobacillus', 'bifidobacterium']
        
        if any(indicator in self.text for indicator in probiotic_indicators) and 'probiotics' not in self.processed_topics:
            self.qas.extend([
                {
                    "instruction": "What are probiotics and how do they help gut health?",
                    "response": "Probiotics are live beneficial bacteria that support your gut health by maintaining a healthy balance in your digestive system. They help with digestion, boost immune function, may reduce inflammation, and can even influence mood through the gut-brain connection. Think of them as reinforcements for your body's natural defense system."
                },
                {
                    "instruction": "What's the best way to get probiotics?",
                    "response": "You can get probiotics through fermented foods like yogurt with live cultures, kefir, sauerkraut, kimchi, and kombucha. Probiotic supplements are also an option, though food sources often provide additional nutrients. Start slowly with fermented foods to let your gut adjust, and choose products with multiple strains of bacteria for the best benefits."
                },
                {
                    "instruction": "How long does it take for probiotics to work?",
                    "response": "Most people start noticing improvements in their digestion within 1-2 weeks of consistently taking probiotics, but it can take 4-6 weeks to see more significant changes in gut health. Everyone's microbiome is unique, so be patient with the process. Consistency is key – think of it as rebuilding your gut's ecosystem rather than a quick fix."
                }
            ])
            
            self.processed_topics.add('probiotics')
    
    def extract_diet_info(self) -> None:
        """Extract information about diet and gut health"""
        diet_keywords = ['diet', 'nutrition', 'fiber', 'processed foods', 'sugar', 'vegetables', 'fruits']
        
        if any(keyword in self.text for keyword in diet_keywords) and 'diet' not in self.processed_topics:
            self.qas.extend([
                {
                    "instruction": "How does diet affect my gut health?",
                    "response": "Your diet is one of the most powerful tools for gut health. A diverse, fiber-rich diet feeds beneficial bacteria, while processed foods and excess sugar can promote harmful bacteria growth. Think of your gut bacteria as a garden – wholesome foods help it flourish, while processed foods can create an imbalanced environment."
                },
                {
                    "instruction": "What foods should I eat for better gut health?",
                    "response": "Focus on fiber-rich foods like vegetables, fruits, whole grains, and legumes. These act as prebiotics, feeding your good bacteria. Include fermented foods for natural probiotics, and add healthy fats from sources like olive oil and avocados. Variety is key – aim for 30 different plant foods per week to support microbial diversity."
                },
                {
                    "instruction": "What foods should I avoid for gut health?",
                    "response": "It's helpful to limit highly processed foods, excess sugar, and artificial sweeteners, as these can disrupt your gut bacteria balance. Everyone's different though – some people are sensitive to gluten, dairy, or certain FODMAPs. Pay attention to how different foods make you feel and consider keeping a food diary to identify your personal triggers."
                }
            ])
            
            self.processed_topics.add('diet')
    
    def extract_microbiome_info(self) -> None:
        """Extract information about gut microbiome"""
        microbiome_keywords = ['microbiome', 'gut bacteria', 'microorganisms', 'bacterial diversity']
        
        if any(keyword in self.text for keyword in microbiome_keywords) and 'microbiome' not in self.processed_topics:
            self.qas.extend([
                {
                    "instruction": "What is the gut microbiome?",
                    "response": "Your gut microbiome is like a bustling city of trillions of microorganisms living in your digestive tract. This complex ecosystem includes bacteria, fungi, and other microbes that work together to help digest food, produce vitamins, regulate your immune system, and even influence your mood. It's truly your body's second brain!"
                },
                {
                    "instruction": "How can I improve my gut microbiome diversity?",
                    "response": "Diversity is the key to a healthy microbiome! Eat a wide variety of plant foods – different types feed different beneficial bacteria. Include fermented foods, limit unnecessary antibiotics, manage stress through relaxation techniques, get quality sleep, and stay active. Each positive choice you make supports your microbial community."
                }
            ])
            
            self.processed_topics.add('microbiome')
    
    def extract_stress_gut_connection(self) -> None:
        """Extract information about stress and gut health"""
        stress_keywords = ['stress', 'anxiety', 'gut-brain', 'mental health', 'mood']
        
        if any(keyword in self.text for keyword in stress_keywords) and 'stress' not in self.processed_topics:
            self.qas.extend([
                {
                    "instruction": "How does stress affect my gut health?",
                    "response": "Stress and gut health are deeply connected through what's called the gut-brain axis. When you're stressed, it can slow digestion, increase inflammation, and alter your gut bacteria composition. This is why you might feel butterflies in your stomach or lose your appetite when anxious. Managing stress isn't just good for your mind – it's essential for your gut too."
                },
                {
                    "instruction": "What can I do to reduce stress for better gut health?",
                    "response": "Great question! Try incorporating stress-reduction techniques like deep breathing, meditation, gentle yoga, or regular walks in nature. Prioritize good sleep, maintain social connections, and consider journaling. Even small changes like eating meals without distractions can help activate your body's 'rest and digest' mode."
                }
            ])
            
            self.processed_topics.add('stress')
    
    def extract_fermented_foods_info(self) -> None:
        """Extract information about fermented foods"""
        fermented_keywords = ['fermented', 'yogurt', 'kefir', 'sauerkraut', 'kimchi', 'kombucha', 'miso']
        
        if any(keyword in self.text for keyword in fermented_keywords) and 'fermented' not in self.processed_topics:
            self.qas.extend([
                {
                    "instruction": "What are the best fermented foods for gut health?",
                    "response": "Wonderful fermented foods to try include yogurt with live cultures, kefir, sauerkraut, kimchi, miso, and kombucha. Each provides different beneficial bacteria strains. Start with small amounts – maybe a few forkfuls of sauerkraut or half a cup of kefir – and gradually increase as your gut adjusts. Your taste buds might need time to appreciate these foods too!"
                },
                {
                    "instruction": "I feel nauseous after eating fermented foods. Is this normal?",
                    "response": "This can happen, and you're not alone in experiencing this! When you introduce fermented foods, especially if you're new to them, your gut bacteria are adjusting to the new arrivals. Try starting with very small amounts, choose milder options like plain yogurt first, and eat them with other foods. If symptoms persist or worsen, take a break and consider consulting a healthcare provider."
                }
            ])
            
            self.processed_topics.add('fermented')
    
    def extract_digestive_issues_info(self) -> None:
        """Extract information about specific digestive issues"""
        digestive_keywords = ['ibs', 'irritable bowel', 'sibo', 'leaky gut', 'inflammatory bowel']
        
        if any(keyword in self.text for keyword in digestive_keywords) and 'digestive_issues' not in self.processed_topics:
            self.qas.extend([
                {
                    "instruction": "What is leaky gut syndrome?",
                    "response": "Leaky gut, or increased intestinal permeability, occurs when the lining of your intestines becomes more porous than normal. This can potentially allow toxins, bacteria, and food particles to pass through into your bloodstream, which may trigger inflammation. While research is ongoing, supporting gut health through diet, stress management, and avoiding excessive alcohol can help maintain a healthy intestinal barrier."
                },
                {
                    "instruction": "How do I know if I have SIBO?",
                    "response": "SIBO (Small Intestinal Bacterial Overgrowth) can cause bloating, gas, abdominal pain, and changes in bowel movements. However, these symptoms overlap with many other conditions, so it's important not to self-diagnose. A healthcare provider can perform specific tests like a hydrogen breath test to determine if you have SIBO. Keep track of your symptoms and discuss them with a professional."
                }
            ])
            
            self.processed_topics.add('digestive_issues')
    
    def extract_healing_signs_info(self) -> None:
        """Extract information about gut healing"""
        healing_keywords = ['healing', 'recovery', 'improvement', 'better digestion']
        
        if any(keyword in self.text for keyword in healing_keywords) and 'healing' not in self.processed_topics:
            self.qas.extend([
                {
                    "instruction": "What are signs that my gut is healing?",
                    "response": "Positive signs include more regular bowel movements, reduced bloating and gas, improved energy levels, better sleep, clearer skin, and improved mood. You might also notice better tolerance of foods that previously caused issues. Healing takes time – typically 4-12 weeks to see significant improvements, so be patient and consistent with healthy habits."
                },
                {
                    "instruction": "How long does it take to heal gut health?",
                    "response": "Gut healing is a gradual process that varies for everyone. Some people notice improvements in digestion within 1-2 weeks, but more significant healing typically takes 6-12 weeks or longer, depending on your starting point and underlying issues. Think of it as nurturing a garden – consistent care over time yields the best results. Stay patient and trust the process."
                }
            ])
            
            self.processed_topics.add('healing')
    
    def add_general_guidance(self) -> None:
        """Add general gut health guidance"""
        if 'general' not in self.processed_topics:
            self.qas.extend([
                {
                    "instruction": "I'm new to focusing on gut health. Where should I start?",
                    "response": "Welcome to your gut health journey! Start simple: eat a variety of colorful fruits and vegetables, drink plenty of water, chew your food slowly, and try to manage stress. Consider adding one fermented food to your diet and focus on getting good sleep. Small, consistent changes are more sustainable than dramatic overhauls."
                },
                {
                    "instruction": "Can antibiotics permanently damage my gut?",
                    "response": "While antibiotics can significantly disrupt your gut bacteria, the damage usually isn't permanent. Your gut microbiome is remarkably resilient and can recover, though it may take several months to fully restore diversity. During and after antibiotic treatment, focus on eating diverse plant foods and consider probiotics (with your doctor's guidance) to support recovery."
                },
                {
                    "instruction": "Should I fast if my gut is inflamed?",
                    "response": "Intermittent fasting might help some people by giving the digestive system a break, but it's not right for everyone, especially if you have certain health conditions. If you're experiencing gut inflammation, it's best to work with a healthcare provider to determine the underlying cause and appropriate treatment. Focus on gentle, anti-inflammatory foods rather than restricting eating entirely."
                }
            ])
            
            self.processed_topics.add('general')
    
    def generate_dataset(self) -> List[Dict]:
        """Generate the complete instruction dataset"""
        print("Analyzing scraped content and generating instruction dataset...")
        
        # Extract information from different categories
        self.extract_symptoms_info()
        self.extract_probiotics_info()
        self.extract_diet_info()
        self.extract_microbiome_info()
        self.extract_stress_gut_connection()
        self.extract_fermented_foods_info()
        self.extract_digestive_issues_info()
        self.extract_healing_signs_info()
        self.add_general_guidance()
        
        print(f"Generated {len(self.qas)} instruction-response pairs")
        print(f"Covered topics: {', '.join(self.processed_topics)}")
        
        return self.qas
    
    def save_dataset(self, output_path: str) -> None:
        """Save the dataset to JSON file"""
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(self.qas, f, indent=2, ensure_ascii=False)
        
        print(f"Dataset saved to {output_path}")
        
        # Print sample for verification
        print("\nSample instruction-response pairs:")
        for i, qa in enumerate(self.qas[:3]):
            print(f"\n{i+1}. Instruction: {qa['instruction']}")
            print(f"   Response: {qa['response'][:100]}...")

def main():
    """Main execution function"""
    try:
        # Initialize generator
        generator = GutHealthDatasetGenerator("data/gut_health_knowledge.txt")
        
        # Generate dataset
        dataset = generator.generate_dataset()
        
        # Save to file
        generator.save_dataset("outputs/gut_health_instruction_dataset_1.json")
        
        print(f"\n✅ Successfully created instruction dataset with {len(dataset)} entries!")
        
    except FileNotFoundError:
        print("❌ Error: data/gut_health_knowledge.txt not found.")
        print("Please run 1_scrape_text.py first to collect the data.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()