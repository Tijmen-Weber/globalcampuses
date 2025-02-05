from dash import Dash


app = Dash(__name__, use_pages=True,external_stylesheets=['styles.css'])



if __name__ == '__main__':
	app.run_server(debug=False)