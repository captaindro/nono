from setuptools import setup, find_packages

setup(
    name="nono-bot",
    version="0.1.0",
    description="Sniper bot Pump.fun Solana with dashboard",
    author="You",
    author_email="you@example.com",
    packages=find_packages(include=["utils", "utils.*"]),
    install_requires=[
<<<<<<< HEAD
        "solana==0.22.0",
=======
        "solana>=0.36.0",       # Mettre une version minimale pour assurer la compatibilité future
        "solders>=0.26.0",      # AJOUTEZ CELA - Essentiel pour la compatibilité avec solana 0.36.x et les méthodes sign/serialize
>>>>>>> 2553739 (Ajout de la config Railway et du workflow CI/CD)
        "websockets<11.0,>=10.1",
        "python-dotenv==1.0.0",
        "ruamel.yaml==0.17.21",
        "requests==2.31.0",
        "numpy>=1.24.0",
<<<<<<< HEAD
        "pydantic<2.0.0",      # <=== pin ici aussi
=======
        "pydantic>=2.0.0",      # C'EST LA LIGNE CLÉ ! Jupiter et les nouvelles solana/solders REQUIÈRENT Pydantic v2+
        "httpx>=0.28.0",        # AJOUTEZ CELA - pour assurer la compatibilité avec Jupiter et pydantic v2+
>>>>>>> 2553739 (Ajout de la config Railway et du workflow CI/CD)
        "fastapi>=0.95.0",
        "uvicorn>=0.22.0"
    ],
    entry_points={
        "console_scripts": [
            "nono=main:main"
        ]
    }
<<<<<<< HEAD
)
=======
)
>>>>>>> 2553739 (Ajout de la config Railway et du workflow CI/CD)
