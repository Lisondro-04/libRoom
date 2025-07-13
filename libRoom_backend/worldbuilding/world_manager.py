import os, json, re
from django.conf import settings
import textwrap



class WorldManager:

    def __init__(self):
        self.project_json_path = settings.PROJECT_JSON_PATH
        self.world_root = self._get_world_path()
        self.index_path = os.path.join(self.world_root, 'world.json')
        self.ensure_structure()

    def _get_world_path(self): 
        if not os.path.exists(self.project_json_path):
            raise FileNotFoundError("No se encontró project.json")
        with open(self.project_json_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        return os.path.join(settings.CURRENT_PROJECT_PATH, project_data.get("world_path", "world"))

    def ensure_structure(self):
        # create base folder if it don't exist
        for folder in ['places', 'objects', 'cities', 'other']:
            path = os.path.join(self.world_root, folder)
            os.makedirs(path, exist_ok=True)

        # create world.json if it don't exist
        if not os.paht.isfile(self.index_path):
            self._write_index({
                "places": [],
                "objects": [],
                "cities":[],
                "custom":[]
            })

    def _read_index(self):
        with open(self.index_path, 'r', encoding='utf-8') as f:
            return json.load(f)
        
    def _write_index(self, data):
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_index(self):
        return self._read_index()
    
    def create_entry(self, category, title):
        index = self._read_index()
        # validate category, if it not existe, add it to custm (other)
        if category not in ['places', 'objects', 'cities', 'custom']:
            category = 'custom'

        #generate an unique id, ex: plc-001, obj-000, cus-001
        prefix_map = {
            'places': 'plc',
            'objects': 'obj',
            'cities': 'cit',
            'custom': 'cus'
        }

        prefix = prefix_map.get(category, 'cus')

        existing = index.get(category, [])
        last_id_num = 0
        for item in existing:
            m = re.match(rf'{prefix}-(\d+)', item['id'])
            if m:
                num = int(m.group(1))
                if num > last_id_num:
                    last_id_num = num
        new_id = f"{prefix}-{last_id_num+1:03d}"

        #normalize filename
        filename = title.lower().replace(' ', '_') + '.md'
        folder = category if category != 'custom' else 'other'
        path = os.path.join(self.world_root, folder, filename)

        # avoid overwrite existing file
        if os.path.exists(path):
            raise FileExistsError(f"The file{filename} already exists in {folder}")
        
        # create file with basic template
        content = textwrap.dedent(f"""\
        Title: {title}
        ID: {new_id}
        Type: {category[:-1] if category != 'custom' else 'custom'}
        Path: {os.path.relpath(path, self.world_root).replace(os.sep, '/')}
        Tags: []
        #Descrption
        """)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # add to index
        entry = {
            "id": new_id,
            "title": title,
            "path": os.path.relpath(path, self.world_root).replace('\\', '/')
        }
        if category not in index:
            index[category] = []
        index[category].append(entry)

        self._write_index(index)
        return entry
    def get_entry_path(self, category, entry_id):
        index = self._read_index()
        category_list = index.get(category)
        if not category_list:
            raise FileNotFoundError("Category not found")
        
        for item in category_list:
            if item['id'] == entry_id:
                return os.path.join(self.world_root, item['path'])
        raise FileNotFoundError(f"Entry with id{entry_id} not found in {category}")
    
    def read_entry(self, category, entry_id):
        path = self.get_entry_path(category, entry_id)
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def write_section(self, category, entry_id, section_name, content):
        path = self.get_entry_path(category, entry_id)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()


        # replace specific seciton (e: # Description)
        # pattern to catch heading and it's content until the next equal heading or higher
        pattern = rf'(#{1,6}{re.scape(section_name)}\s*\n)(.*?)(?=\n#{1,6} |\Z)'
        match = re.search(pattern, text, flags=re.DOTALL)
        if not match:
            # if section don't exist, add it at the end
            text += f"\n# {section_name}\n{content}\n"
        else:
            start, end = match.span(2)
            text = text[:start] + content + text[end:]
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)

    def delete_entry(self, category, entry_id):
        index = self._read_index()
        if category not in index:
            raise FileNotFoundError("This category doesn't exist in the index")
        
        entry_list = index[category]
        entry = next((e for e in entry_list if e['id']== entry_id), None)
        if not entry:
            raise FileNotFoundError("Entry not found")
        
        # delete file
        path = os.path.join(self.world_root, entry['path'])
        if os.path.exists(path):
            os.remove(path)

        # delete the index
        index[category] = [e for e in entry_list if e['id'] != entry_id]
        self._write_index(index)

