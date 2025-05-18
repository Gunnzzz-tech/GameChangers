from flask import Flask, render_template
import folium
app = Flask(__name__)


# Center the map around J P Nagar
map_center = [12.905, 77.555]
crime_map = folium.Map(location=map_center, zoom_start=13)

# Your crime list
crime_data = [
    {"type": "assault", "lat": 12.88744307, "lon": 77.56855708},
    {"type": "assault", "lat": 12.911738, "lon": 77.556877},
    {"type": "assault", "lat": 12.89033243, "lon": 77.56334831},
    {"type": "assault", "lat": 12.91707248, "lon": 77.54891947},
    {"type": "assault", "lat": 12.90518454, "lon": 77.54469773},
    {"type": "assault", "lat": 12.90557877, "lon": 77.55645958},
{"type": "assault", "lat": 12.920604, "lon": 77.520557},
    {"type": "murder", "lat": 12.940662, "lon": 77.574095},
    {"type": "assault", "lat": 12.93878218, "lon": 77.57956109},
    {"type": "murder", "lat": 12.9399013, "lon": 77.57337112},
    {"type": "assault", "lat": 12.944557, "lon": 77.57758},
    {"type": "murder", "lat": 12.9076508, "lon": 77.5951967},
    {"type": "assault", "lat": 12.9076508, "lon": 77.5951967},
    {"type": "murder", "lat": 12.9030543, "lon": 77.5813948},
    {"type": "assault", "lat": 12.9036647, "lon": 77.5785439},
    {"type": "murder", "lat": 12.9004589, "lon": 77.5684636},
    {"type": "assault", "lat": 12.909427, "lon": 77.5706543},
    {"type": "murder", "lat": 12.9039655, "lon": 77.5804308},
    {"type": "assault", "lat": 12.9039653, "lon": 77.5738647},
    {"type": "murder", "lat": 12.9124543, "lon": 77.5737283},
    {"type": "assault", "lat": 12.9108342, "lon": 77.5866704},
    {"type": "murder", "lat": 12.9071236, "lon": 77.583816},
    {"type": "assault", "lat": 12.917125, "lon": 77.568519},
    {"type": "murder", "lat": 12.915422, "lon": 77.562005},
{"type": "murder", "lat": 12.859739, "lon": 77.562719},
  {"type": "murder", "lat": 12.862041, "lon": 77.563487},
  {"type": "murder", "lat": 12.893051, "lon": 77.543007},
  {"type": "murder", "lat": 12.879223, "lon": 77.567169},
  {"type": "murder", "lat": 12.882152, "lon": 77.565325},
  {"type": "murder", "lat": 12.84488, "lon": 77.583729},
  {"type": "murder", "lat": 12.890277, "lon": 77.57144},
  {"type": "murder", "lat": 12.885583, "lon": 77.57054},
  {"type": "murder", "lat": 12.889932, "lon": 77.57465},
  {"type": "murder", "lat": 12.861345, "lon": 77.579767},
  {"type": "murder", "lat": 12.845887, "lon": 77.583885},
  {"type": "murder", "lat": 12.873733, "lon": 77.579546},
  {"type": "murder", "lat": 12.899989, "lon": 77.573775},
  {"type": "murder", "lat": 12.875176, "lon": 77.57889},
  {"type": "murder", "lat": 12.898898, "lon": 77.576405},
  {"type": "murder", "lat": 12.906331, "lon": 77.59179},
  {"type": "murder", "lat": 12.90903, "lon": 77.58764},
  {"type": "murder", "lat": 12.906448, "lon": 77.587569},
  {"type": "murder", "lat": 12.89643, "lon": 77.578607},
  {"type": "murder", "lat": 12.901612, "lon": 77.586583}

]
crime_map.save("bangalore_crime_map.html")



police_stations = [
    {
        "name": "18 Radhakrishna Temple, Hebbal",
        "lat": 13.039596,
        "lon": 77.564157
    },
    {
        "name": "19 Sanjaynagar, Hebbal",
        "lat": 13.0338,
        "lon": 77.576072
    },
    {
        "name": "20 Ganganagar, Hebbal",
        "lat": 13.026323,
        "lon": 77.584997
    },
    {
        "name": "21 Hebbala, Hebbal",
        "lat": 13.030312,
        "lon": 77.587162
    },
    {
        "name": "22 Nagenahalli, Hebbal",
        "lat": 13.026224,
        "lon": 77.585123
    },
    {
        "name": "34 Gangenahalli, Hebbal",
        "lat": 13.020334,
        "lon": 77.592086
    },
    {
        "name": "46 Jayachamarajendra Nagar, Hebbal",
        "lat": 13.00634,
        "lon": 77.593513
    },
    {
        "name": "62 Ramaswamy Palya, Shivajinagar",
        "lat": 13.001508,
        "lon": 77.601396
    },
    {
        "name": "63 Jayamahal, Shivajinagar",
        "lat": 13.00153,
        "lon": 77.601542
    },
    {
        "name": "91 Bharathinagar, Shivajinagar",
        "lat": 12.98429,
        "lon": 77.605431
    },
    {
        "name": "92 Shivajinagar, Shivajinagar",
        "lat": 12.98842,
        "lon": 77.604328
    },
    {
        "name": "93 Vasanthanagar, Shivajinagar",
        "lat": 12.989256,
        "lon": 77.597329
    },
    {
        "name": "110 Sampangiramanagar, Shivajinagar",
        "lat": 12.967327,
        "lon": 77.587111
    },
{
    "name": "118 Sudhamanagar",
    "lat": 12.953059,
    "lon": 77.573855
  },
  {
    "name": "119 Dharmarayaswamy Temple",
    "lat": 12.964545,
    "lon": 77.57662
  },
  {
    "name": "142 Sukenahalli",
    "lat": 12.950233,
    "lon": 77.564395
  },
  {
    "name": "143 Vishveshwarapuram",
    "lat": 12.9530944,
    "lon": 77.5739307
  },
  {
    "name": "144 Siddapura",
    "lat": 12.936628,
    "lon": 77.597319
  },
  {
    "name": "145 Hombegowdanagar",
    "lat": 12.950332,
    "lon": 77.598113
  },
  {
    "name": "153 Jayanagar",
    "lat": 12.943434,
    "lon": 77.583065
  },
  {
    "name": "168 Pattabhi Nagar",
    "lat": 12.927036,
    "lon": 77.59316
  },
  {
    "name": "169 Byesandra",
    "lat": 12.936232,
    "lon": 77.592634
  },
  {
    "name": "170 Jayanagara East mobile IC",
    "lat": 12.92129,
    "lon": 77.596967
  },
  {
    "name": "171 Gurappanapalya",
    "lat": 12.926962,
    "lon": 77.60127
  },
  {
    "name": "177 JP Nagar mobile IC",
    "lat": 12.910176,
    "lon": 77.594716
  },
  {
    "name": "178 Sarakki",
    "lat": 12.907278,
    "lon": 77.57895
  },
  {
    "name": "179 Sakrembi Nagar",
    "lat": 12.917376,
    "lon": 77.57456
  },
  {
    "name": "161 Hosakerehalli",
    "lat": 12.931149,
    "lon": 77.539956
  },
  {
    "name": "166 Karisandra",
    "lat": 12.916981,
    "lon": 77.573601
  },
  {
    "name": "180 Banashankari Temple Ward",
    "lat": 12.91391,
    "lon": 77.567094
  },
  {
    "name": "183 Chikkalasandra",
    "lat": 12.926288,
    "lon": 77.547666
  },
  {
    "name": "123 Vijayanagar",
    "lat": 12.973351,
    "lon": 77.541328
  },
  {
    "name": "124 Hosahalli",
    "lat": 12.96671,
    "lon": 77.543927
  },
  {
    "name": "132 Athiguppe",
    "lat": 12.9579829,
    "lon": 77.5273219
  },
  {
    "name": "133 Hampinagar",
    "lat": 12.958718,
    "lon": 77.535697
  },
  {
    "name": "157 Gali Anjaneya Temple",
    "lat": 12.945858,
    "lon": 77.54851
  },
  {
    "name": "158 Deepanjalinagar",
    "lat": 12.936372,
    "lon": 77.534911
  },
  {
    "name": "25 Horamavu",
    "lat": 13.026726,
    "lon": 77.66564
  },
{
    "name": "73 Kottegepalya",
    "lat": 12.97953,
    "lon": 77.516823
  },
  {
    "name": "160 Rajarajeshwarinagar",
    "lat": 12.925145,
    "lon": 77.527429
  },
  {
    "name": "40 Doddabidarakalu",
    "lat": 13.016372,
    "lon": 77.483332
  },
  {
    "name": "72 Herohalli",
    "lat": 12.98602,
    "lon": 77.477654
  },
  {
    "name": "130 Ullalu",
    "lat": 12.950406,
    "lon": 77.491886
  },
  {
    "name": "159 Kengeri",
    "lat": 12.914341,
    "lon": 77.481742
  },
  {
    "name": "198 Hemigepura",
    "lat": 12.903698,
    "lon": 77.510864
  },
  {
    "name": "1 Kempegowda Ward",
    "lat": 13.097495,
    "lon": 77.599465
  },
  {
    "name": "2 Chowdeshwari Ward",
    "lat": 13.104665,
    "lon": 77.594842
  },
  {
    "name": "3 Attur",
    "lat": 13.100741,
    "lon": 77.576676
  },
  {
    "name": "4 Yelahanka Satellite Town",
    "lat": 13.099375,
    "lon": 77.588232
  },
  {
    "name": "5 Jakkur",
    "lat": 13.10356,
    "lon": 77.616241
  },
  {
    "name": "6 Thanisandra",
    "lat": 13.073584,
    "lon": 77.633839
  },
{
  "name": "7 Bytarayanapura",
  "lat": 13.057452,
  "lon": 77.597653
},
{
  "name": "8 Kodigehalli",
  "lat": 13.053472,
  "lon": 77.574826
},
{
  "name": "9 Vidyaranyapura",
  "lat": 13.076583,
  "lon": 77.55025
},
{
  "name": "10 Doddabommasandra",
  "lat": 13.053492,
  "lon": 77.574819
},
{
  "name": "11 Kuvempunagara",
  "lat": 13.080185,
  "lon": 77.539154
},
{
  "name": "184 Uttarahalli",
  "lat": 12.893141,
  "lon": 77.543057
},
{
  "name": "185 Yelachenahalli mobile IC",
  "lat": 12.899527,
  "lon": 77.56503
},
{
  "name": "191 Singasandra",
  "lat": 12.892827,
  "lon": 77.673451
},
{
  "name": "192 Begur",
  "lat": 12.878286,
  "lon": 77.624616
},
{
  "name": "194 Gottigere",
  "lat": 12.865173,
  "lon": 77.581491
},
{
  "name": "195 Konanakunte",
  "lat": 12.884445,
  "lon": 77.56621
},
{
  "name": "196 Anjanapura",
  "lat": 12.863002,
  "lon": 77.564722
},
{
  "name": "197 Vasanthapura",
  "lat": 12.896157,
  "lon": 77.550468
},
{
  "name": "193 Arakere",
  "lat": 12.883643,
  "lon": 77.60527
},
{
  "name": "186 Jaraganahalli",
  "lat": 12.872106,
  "lon": 77.599908
},
{
  "name": "187 Puttenahalli",
  "lat": 12.895191,
  "lon": 77.599099
},
{
  "name": "188 Bilekahalli",
  "lat": 12.894559,
  "lon": 77.611521
},
{
  "name": "189 Hongasandra",
  "lat": 12.905041,
  "lon": 77.64255
},
{
  "name": "190 Mangamanapalya",
  "lat": 12.896229,
  "lon": 77.641224
},
{
  "name": "174 H.S.R.Layout",
  "lat": 12.923068,
  "lon": 77.6643
},
{
  "name": "175 Bommanahalli",
  "lat": 12.893113,
  "lon": 77.616616
}


]
crime = [
    {
        "type": "assault",
        "lat": 12.88744307,
        "lon": 77.56855708
    },
    {
        "type": "assault",
        "lat": 12.911738,
        "lon": 77.556877
    },
    {
        "type": "assault",
        "lat": 12.89033243,
        "lon": 77.56334831
    },
    {
        "type": "assault",
        "lat": 12.91707248,
        "lon": 77.54891947
    },
    {
        "type": "assault",
        "lat": 12.90518454,
        "lon": 77.54469773
    },
    {
        "type": "assault",
        "lat": 12.90557877,
        "lon": 77.55645958
    },

    {"type": "murder", "lat": 12.924377, "lon": 77.582729},


]

# ]

for crime in crime_data:
    folium.Marker(
        location=[crime["lat"], crime["lon"]],
        popup=f"Crime Type: {crime['type']}",
        icon=folium.Icon(color="red", icon="exclamation-sign")
    ).add_to(crime_map)

# Add police station markers
for station in police_stations:
    folium.Marker(
        location=[station["lat"], station["lon"]],
        popup=f"Police Station: {station['name']}",
        icon=folium.Icon(color="red", icon="glyphicon glyphicon-tower")  # Red icon for now
    ).add_to(crime_map)

@app.route("/")
def home():
    return render_template("index.html", police_stations=police_stations)

if __name__ == "__main__":
    app.run(debug=True)
