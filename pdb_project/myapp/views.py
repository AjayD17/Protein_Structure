# PDB_STRUCTURES:
import requests
from django.shortcuts import render, redirect

def view_protein(request):
    pdb_id = request.GET.get('pdb_id', '').lower()
    protein_info = {}

    if pdb_id:
        # Fetch basic structure info from RCSB PDB REST API
        url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            protein_info = {
                'title': data.get('struct', {}).get('title', 'N/A'),
                'method': data.get('exptl', [{}])[0].get('method', 'N/A'),
                'resolution': data.get('rcsb_entry_info', {}).get('resolution_combined', ['N/A'])[0],
                'deposition_date': data.get('rcsb_accession_info', {}).get('deposit_date', 'N/A'),
                'release_date': data.get('rcsb_accession_info', {}).get('initial_release_date', 'N/A'),
                'authors': ', '.join(set(author.get('name', 'N/A') for author in data.get('audit_author', [])))
            }
        else:
            protein_info = {'error': f"Protein with ID '{pdb_id.upper()}' not found."}

    return render(request, 'index.html', {'pdb_id': pdb_id.upper(), 'protein_info': protein_info})

