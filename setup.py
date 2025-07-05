from setuptools import setup, find_packages

setup(
    name="nono-bot",
    version="0.1.0",
    description="Sniper bot Pump.fun Solana with dashboard",
    author="You",
    author_email="you@example.com",
    packages=find_packages(include=["utils", "utils.*"]),
    install_requires=[
        "solana==0.22.0",
        "websockets<11.0,>=10.1",
        "python-dotenv==1.0.0",
        "ruamel.yaml==0.17.21",
        "requests==2.31.0",
        "numpy>=1.24.0",
        "pydantic<2.0.0",      # <=== pin ici aussi
        "fastapi>=0.95.0",
        "uvicorn>=0.22.0"
    ],
    entry_points={
        "console_scripts": [
            "nono=main:main"
        ]
    }
)
