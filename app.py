from flask import Flask, render_template
from models import CountryTab, WorldTab, db, init_db
from flask_migrate import Migrate
from flask import request
from sqlalchemy import func

import csv
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
init_db(app)
migrate = Migrate(app, db)

def load_data(model, filename):
    with app.app_context():
        db.create_all()
        data = pd.read_csv(filename, sep=";", encoding="ISO-8859-1")
        data.to_sql(model.__tablename__, db.engine, if_exists='replace', index=False)

load_data(CountryTab, 'Country.csv')
load_data(WorldTab, 'World.csv')

@app.route("/",methods=["GET", "POST"])
def index():
    try:

        sql_query = db.session.query(CountryTab).limit(5)
        results = sql_query.all()
        query_results = [dict(result.__dict__) for result in results]

        sql_query1 = db.session.query(WorldTab).limit(5)
        results1 = sql_query1.all()
        query_results1 = [dict(result.__dict__) for result in results1] 

        sql_query_coal = db.session.query(CountryTab.Country, CountryTab.Coal).filter(CountryTab.Coal.is_not(None)).order_by(CountryTab.Coal.desc()).limit(1)
        sql_query_gas = db.session.query(CountryTab.Country, CountryTab.Gas).filter(CountryTab.Gas.is_not(None)).order_by(CountryTab.Gas.desc()).limit(1)
        sql_query_oil = db.session.query(CountryTab.Country, CountryTab.Oil).filter(CountryTab.Oil.is_not(None)).order_by(CountryTab.Oil.desc()).limit(1)
        sql_query_hydro = db.session.query(CountryTab.Country, CountryTab.Hydro).filter(CountryTab.Hydro.is_not(None)).order_by(CountryTab.Hydro.desc()).limit(1)
        sql_query_renewable = db.session.query(CountryTab.Country, CountryTab.Renewable).filter(CountryTab.Renewable.is_not(None)).order_by(CountryTab.Renewable.desc()).limit(1)
        sql_query_nuclear = db.session.query(CountryTab.Country, CountryTab.Nuclear).filter(CountryTab.Nuclear.is_not(None)).order_by(CountryTab.Nuclear.desc()).limit(1)

        return render_template("index.html", query_results=query_results, query_results1=query_results1,sql_query_coal=sql_query_coal, sql_query_gas=sql_query_gas, sql_query_oil=sql_query_oil, sql_query_hydro=sql_query_hydro, sql_query_renewable=sql_query_renewable, sql_query_nuclear=sql_query_nuclear)

    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"

@app.route('/test', methods=['GET', 'POST'])
def test():
    try:
        # Requête pour le pays avec le plus d'émissions globales
        sql_query = db.session.query(CountryTab.Country,
                                     func.sum(CountryTab.Coal + CountryTab.Gas + CountryTab.Oil +
                                              CountryTab.Hydro + CountryTab.Renewable + CountryTab.Nuclear)
                                     .label("TotalEmissions"))
        result = sql_query.group_by(CountryTab.Country).order_by(CountryTab.Country).first()
        highest_emitting_country = {"Country": result.Country, "TotalEmissions": result.TotalEmissions}

        return render_template("test.html", highest_emitting_country=highest_emitting_country)
    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    try:
        # Requête pour obtenir les émissions totales mondiales
        sql_query_world = db.session.query(func.sum(WorldTab.Coal + WorldTab.Gas + WorldTab.Oil +
                                                   WorldTab.Hydro + WorldTab.Renewable + WorldTab.Nuclear)
                                          .label("TotalWorldEmissions"))
        total_world_emissions_result = sql_query_world.one()
        total_world_emissions = total_world_emissions_result.TotalWorldEmissions

        # Requête pour obtenir les émissions totales par pays
        sql_query_countries = db.session.query(CountryTab.Country,
                                               func.sum(CountryTab.Coal + CountryTab.Gas + CountryTab.Oil +
                                                        CountryTab.Hydro + CountryTab.Renewable + CountryTab.Nuclear)
                                               .label("TotalEmissions"))
        total_emissions_by_country = sql_query_countries.group_by(CountryTab.Country).all()
        total_emissions_by_country_results = [{"Country": result.Country, "TotalEmissions": result.TotalEmissions}
                                               for result in total_emissions_by_country]

        # Requête pour obtenir le pays avec les émissions les plus élevées
        sql_query_highest_emitting_country = db.session.query(CountryTab.Country,
                                                              func.sum(CountryTab.Coal + CountryTab.Gas + CountryTab.Oil +
                                                                       CountryTab.Hydro + CountryTab.Renewable + CountryTab.Nuclear)
                                                              .label("TotalEmissions"))
        highest_emitting_country_result = sql_query_highest_emitting_country.group_by(CountryTab.Country).order_by(CountryTab.Country).first()
        highest_emitting_country = {"Country": highest_emitting_country_result.Country,
                                    "TotalEmissions": highest_emitting_country_result.TotalEmissions}

        # Requête pour obtenir les émissions de charbon
        sql_query_coal = db.session.query(CountryTab.Country, CountryTab.Coal).filter(CountryTab.Coal.isnot(None)).order_by(CountryTab.Coal.desc()).limit(1)
        sql_query_gas = db.session.query(CountryTab.Country, CountryTab.Gas).filter(CountryTab.Gas.isnot(None)).order_by(CountryTab.Gas.desc()).limit(1)
        sql_query_oil = db.session.query(CountryTab.Country, CountryTab.Oil).filter(CountryTab.Oil.isnot(None)).order_by(CountryTab.Oil.desc()).limit(1)
        sql_query_hydro = db.session.query(CountryTab.Country, CountryTab.Hydro).filter(CountryTab.Hydro.isnot(None)).order_by(CountryTab.Hydro.desc()).limit(1)
        sql_query_renewable = db.session.query(CountryTab.Country, CountryTab.Renewable).filter(CountryTab.Renewable.isnot(None)).order_by(CountryTab.Renewable.desc()).limit(1)
        sql_query_nuclear = db.session.query(CountryTab.Country, CountryTab.Nuclear).filter(CountryTab.Nuclear.isnot(None)).order_by(CountryTab.Nuclear.desc()).limit(1)

        return render_template("analysis.html", total_world_emissions=total_world_emissions,
                               total_emissions_by_country_results=total_emissions_by_country_results,
                               highest_emitting_country=highest_emitting_country,
                               sql_query_coal=sql_query_coal, sql_query_gas=sql_query_gas,
                               sql_query_oil=sql_query_oil, sql_query_hydro=sql_query_hydro,
                               sql_query_renewable=sql_query_renewable, sql_query_nuclear=sql_query_nuclear)

    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"

# Définir les valeurs médianes du tableau directement dans le code
co2_emissions = {
    "Coal": 820,
    "Gas": 490,
    "Oil": 740,
    "Hydro": 24,
    "Renewable": 41,
    "Nuclear": 12,
}

@app.route('/contribution', methods=['GET', 'POST'])
def contribution():
    try:
        # Récupérer les données de la table
        countries = db.session.query(CountryTab).all()

        # Initialiser la liste pour stocker les résultats sous forme de dictionnaires
        total_impact_results = []

        for source, median_value in co2_emissions.items():
            # Calculer l'impact total pour chaque source en parcourant tous les pays
            total_impact = sum((getattr(country, source) * median_value) / 100 for country in countries)

            # Stocker les résultats dans la liste
            total_impact_results.append({"Source": source, "Valeur": total_impact})

        return render_template("contribution.html", total_impact_results=total_impact_results)

    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"

@app.route('/contribution_filtered', methods=['GET', 'POST'])
def contribution_filtered():
    try:
        # Récupérer la liste distincte des pays pour la sélection box
        distinct_countries = [country.Country for country in db.session.query(CountryTab.Country).distinct()]

        countries = db.session.query(CountryTab).all()

        # Initialiser la liste pour stocker les résultats sous forme de dictionnaires
        total_impact_results = []

        # Vérifier si une sélection de pays a été soumise
        selected_country = request.form.get('selected_country')

        # Si un pays est sélectionné, filtrer les données par pays
        if selected_country:
            filtered_countries = [country for country in countries if country.Country == selected_country]
        else:
            filtered_countries = countries
        
        total_impact_results=[]

        # Calcule de l'impact total pour chaque source en parcourant les pays filtrés
        for source, median_value in co2_emissions.items():
            total_impact = sum((getattr(country, source) * median_value) / 100 for country in filtered_countries)
            percentage= 0 if total_impact == 0 else (getattr(filtered_countries[0], source) * median_value) / total_impact
            contribution = percentage * median_value

            total_impact_results.append({
                "Source": source,
                "Percentage": percentage,
                "Median": int(median_value),
                "Contribution": int(contribution)
                })
        # Calcule de l'émission totale de CO2 pour le pays sélectionné
        total_emission = sum(getattr(filtered_countries[0], source) for source in co2_emissions)

        trees_needed = total_emission / 25  # 25 kg de CO2 absorbés par un arbre par an
        return render_template("contribution_filtered.html",
                                total_impact_results=total_impact_results,
                                distinct_countries=distinct_countries,
                                selected_country=selected_country,
                                total_emission=total_emission,
                                trees_needed=trees_needed)                   

    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
