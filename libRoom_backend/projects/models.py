from django.db import models
import json

class Project: 
    def __init__(self, path):
        self.path = path
        self.project_file = path / "project.json"
    def load(self):
        with open(self.project_file, 'r') as f:
            return json.load(f)
        
    def save (self, data):
        with open(self.project_file, 'w') as f:
            json.dump(data, f, indent=2)
