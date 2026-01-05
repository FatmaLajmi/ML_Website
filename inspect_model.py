"""
Script pour inspecter le modèle et voir les catégories attendues
"""
import joblib
from pathlib import Path

model_path = Path("ml_models/models/remote_work_v3(eya).pkl")
model = joblib.load(model_path)

print("=" * 70)
print("INSPECTION DU MODÈLE")
print("=" * 70)

print(f"\nType du modèle: {type(model)}")
print(f"\nSteps du pipeline:")
for name, step in model.named_steps.items():
    print(f"  - {name}: {type(step)}")

# Chercher le ColumnTransformer et ses catégories
print("\n" + "-" * 70)
print("RECHERCHE DES CATÉGORIES ATTENDUES")
print("-" * 70)

if hasattr(model, 'named_steps'):
    for step_name, step in model.named_steps.items():
        if 'preprocess' in step_name.lower() or 'transform' in step_name.lower():
            print(f"\nStep: {step_name}")
            print(f"Type: {type(step)}")
            
            # Si c'est un ColumnTransformer
            if hasattr(step, 'transformers_'):
                print("Transformers trouvés:")
                for transformer_name, transformer, columns in step.transformers_:
                    print(f"  - {transformer_name}: {columns}")
                    
                    # Si c'est un OneHotEncoder
                    if hasattr(transformer, 'named_steps'):
                        for t_name, t_step in transformer.named_steps.items():
                            if hasattr(t_step, 'categories_'):
                                print(f"    - {t_name} categories:")
                                for i, col in enumerate(columns):
                                    if i < len(t_step.categories_):
                                        print(f"      {col}: {list(t_step.categories_[i])}")
                    elif hasattr(transformer, 'categories_'):
                        print(f"    Catégories OneHotEncoder:")
                        if hasattr(transformer, 'get_feature_names_out'):
                            try:
                                features = transformer.get_feature_names_out(columns)
                                print(f"    Feature names: {features}")
                            except:
                                pass
                        for i, col in enumerate(columns):
                            print(f"      {col}: {list(transformer.categories_[i])}")

print("\n" + "=" * 70)
print("ESSAYEZ AVEC CES VALEURS POUR TEST")
print("=" * 70)
print("""
Créez des données avec les valeurs acceptées par le modèle.
Exemples possibles:
- job_title_short: "data scientist", "software engineer", etc.
- job_seniority: "junior", "mid", "senior", etc.
- job_country: "US", "FR", "UK", etc.
- job_schedule_type: "full-time", "part-time", "contract", etc.
""")
