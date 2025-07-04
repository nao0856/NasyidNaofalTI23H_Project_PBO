# models/war_models.py
from abc import ABC, abstractmethod
import json

# Abstract Class untuk memenuhi syarat Polymorphism
class War(ABC):
    def __init__(self, opponent_clan, war_size):
        self.opponent_clan = opponent_clan
        self.war_size = war_size

    @abstractmethod
    def display_summary(self):
        """Metode abstrak untuk menampilkan ringkasan."""
        pass

# Class untuk Partisipan War
# Class ini hanya akan digunakan sebagai struktur data di dalam Python,
# tidak memiliki tabel sendiri di database.
class WarParticipant:
    def __init__(self, name, th_level):
        self.name = name
        self.th_level = th_level
        self.attacks = [] # List untuk menyimpan catatan serangan (string)

    def add_attack(self, note):
        if len(self.attacks) < 2:
            self.attacks.append(note)
            return True
        return False
    
    # Method untuk mengubah objek menjadi dictionary (untuk disimpan sebagai JSON)
    def to_dict(self):
        return {"name": self.name, "th_level": self.th_level, "attacks": self.attacks}

# Class Konkret yang mewarisi dari 'War'
class RegularWar(War):
    # Konstruktor menerima semua atribut, termasuk 'id' dari database
    def __init__(self, opponent_clan, war_size, start_date, status="Preparation", participants=None, war_id=None):
        super().__init__(opponent_clan, war_size)
        self.id = war_id
        self.start_date = start_date
        self.status = status
        self.participants = participants if participants is not None else []
    
    def add_participant(self, participant):
        if len(self.participants) < self.war_size:
            self.participants.append(participant)
    
    def display_summary(self):
        """Implementasi konkret dari metode abstrak."""
        print("-" * 30)
        print(f"War ID: {self.id} | Lawan: {self.opponent_clan}")
        print(f"Ukuran: {self.war_size} vs {self.war_size} | Status: {self.status}")
        print("Peserta:")
        if not self.participants:
            print("  (Belum ada peserta)")
        for p in self.participants:
            print(f"  - {p.name} (TH{p.th_level}), Serangan: {len(p.attacks)}/2")
            for attack_note in p.attacks:
                print(f"    * {attack_note}")
        print("-" * 30)

    # -- Metode Interaksi Database --
    
    def save(self, conn):
        """Menyimpan atau memperbarui data war ke database."""
        cursor = conn.cursor()
        
        # Ubah list objek partisipan menjadi JSON string
        participants_json = json.dumps([p.to_dict() for p in self.participants])
        
        if self.id is None:
            # Jika war baru (id belum ada), lakukan INSERT
            query = """
                INSERT INTO wars (opponent_clan, war_size, start_date, status, participants_data)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (self.opponent_clan, self.war_size, self.start_date, self.status, participants_json))
            self.id = cursor.lastrowid # Ambil ID yang baru dibuat
        else:
            # Jika war sudah ada, lakukan UPDATE
            query = """
                UPDATE wars SET opponent_clan=%s, war_size=%s, start_date=%s, status=%s, participants_data=%s
                WHERE id=%s
            """
            cursor.execute(query, (self.opponent_clan, self.war_size, self.start_date, self.status, participants_json, self.id))
        
        conn.commit()
        cursor.close()

    @staticmethod
    def get_all(conn):
        """Mengambil semua data war dari database dan mengubahnya menjadi objek RegularWar."""
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM wars ORDER BY start_date DESC")
        rows = cursor.fetchall()
        cursor.close()
        
        wars_list = []
        for row in rows:
            participants_list = []
            if row['participants_data']:
                # Ubah JSON string dari DB kembali menjadi list of dictionary
                participants_data = json.loads(row['participants_data'])
                for p_data in participants_data:
                    # Buat objek WarParticipant
                    participant = WarParticipant(p_data['name'], p_data['th_level'])
                    participant.attacks = p_data.get('attacks', [])
                    participants_list.append(participant)

            # Buat objek RegularWar dari data baris
            war = RegularWar(
                war_id=row['id'],
                opponent_clan=row['opponent_clan'],
                war_size=row['war_size'],
                start_date=str(row['start_date']),
                status=row['status'],
                participants=participants_list
            )
            wars_list.append(war)
        return wars_list