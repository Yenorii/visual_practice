import pandas as pd

# Read the CSV file and filter data for the USA
uscoordinates = pd.read_csv('coordinates.csv')[['usa_state_code', 'usa_state_latitude', 'usa_state_longitude', 'usa_state']].dropna()

# Rename columns
uscoordinates.rename(columns={'usa_state_latitude': 'latitude', 'usa_state_longitude': 'longitude', 'usa_state_code': 'state_code', 'usa_state': 'state'}, inplace=True)

# Display the filtered data
print(uscoordinates)

# Save the filtered data to a new CSV file
uscoordinates.to_csv('uscoordinates.csv', index=False)

# Generate HTML dropdown options within the script
selector_options = '\n'.join([f'<option value="{state}">{state}</option>' for state in uscoordinates['state'].unique()])

# Create HTML content
html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>US Map with State Select</title>
    <!-- Leaflet CSS and JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    <style>
        #map {{
            height: 400px;
        }}
    </style>
</head>
<body>

<div>
    <label for="stateSelect">Select a State:</label>
    <select id="stateSelect" onchange="updateMap()">
        <option value="default">Select a State</option>
        {selector_options}
    </select>
</div>

<div id="map"></div>

<script>
    var map = L.map('map').setView([37.8, -96], 4);

    L.tileLayer('https://(s).tile.openstreetmap.org/(z)/(x)/(y).png').addTo(map);

    var data = {uscoordinates.to_dict(orient='records')};

    // Function to update the map based on the selected state
    function updateMap() {{
        var selectedState = document.getElementById('stateSelect').value;

        // Check if a valid state is selected
        if (selectedState !== 'default') {{
            // Filter data for the selected state
            var selectedData = data.find(item => item.state === selectedState);

            // Set the map view to the selected state's coordinates
            map.setView([selectedData.latitude, selectedData.longitude], 8);
        }}
    }}
</script>

</body>
</html>
'''

# Save the HTML content to a file
with open('index.html', 'w') as file:
    file.write(html_content)