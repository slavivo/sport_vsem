const districtDict = {
    'praha': 'Praha',
    'stredocesky': 'Středočeský kraj',
    'jihocesky': 'Jihočeský kraj',
    'plzen': 'Plzeňský kraj',
    'karlovarsky': 'Karlovarský kraj',
    'ustecky': 'Ústecký kraj',
    'liberec': 'Liberecký kraj',
    'kralovehradecky': 'Královéhradecký kraj',
    'pardubicky': 'Pardubický kraj',
    'vysocina': 'Kraj Vysočina',
    'jihomoravsky': 'Jihomoravský kraj',
    'olomouc': 'Olomoucký kraj',
    'moravskoslezsky': 'Moravskoslezský kraj',
    'zlin': 'Zlínský kraj'
};

async function loadDistrictData() {
    const urlParams = new URLSearchParams(window.location.search);
    const district = urlParams.get('district');
    
    if (!district) {
        window.location.href = 'index.html';
        return;
    }

    const districtTitle = document.getElementById('district-title');
    districtTitle.textContent = districtDict[district] || district;

    try {
        const response = await fetch('static/data/samples.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        const samples = data[district] || [];
        
        const container = document.getElementById('locations-container');
        container.className = 'locations-container'; // Add the class that matches your CSS

        if (samples.length === 0) {
            container.innerHTML = '<p>Žádná data pro tento kraj nejsou k dispozici.</p>';
            return;
        }

        samples.forEach(sample => {
            const card = createLocationCard(sample);
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('locations-container').innerHTML = 
            '<p>Nepodařilo se načíst data. Prosím zkuste to později.</p>';
    }
}

function createLocationCard(sample) {
    const card = document.createElement('div');
    card.className = 'location-card';
    
    // Recreate the exact structure from your original Markdown template
    card.innerHTML = `
        <div class="location-details">
            <h2>${sample.name}</h2>
            <p><strong>Stránka:</strong> ${sample.webpage && sample.webpage !== '-' ? 
                `<a href="${sample.webpage}" target="_blank">${sample.webpage}</a>` : 
                sample.webpage || '-'}</p>
            <p><strong>Kontakt:</strong> ${sample.contact || '-'}</p>
            <p><strong>Email:</strong> ${sample.email || '-'}</p>
            <p><strong>Tel.:</strong> ${sample.tel || '-'}</p>
        </div>
        <div class="additional-info">
            <h2>&nbsp;</h2>
            <p><strong>Aktivity:</strong> ${sample.activities || '-'}</p>
            <p><strong>Adresa:</strong> ${sample.address || '-'}</p>
            <p><strong>Členství:</strong> ${sample.membership || '-'}</p>
        </div>
    `;
    
    return card;
}

document.addEventListener('DOMContentLoaded', loadDistrictData);