"""
Comando de gestión para poblar la base de datos con juegos de ejemplo
"""
from django.core.management.base import BaseCommand
from tienda.models import Juego


class Command(BaseCommand):
    help = 'Pobla la base de datos con juegos de ejemplo del Xbox 360'

    def handle(self, *args, **options):
        juegos_ejemplo = [
            {
                'titulo': 'Halo 3',
                'descripcion': 'La épica conclusión de la trilogía original de Halo. Únete al Jefe Maestro en su batalla final contra el Covenant y los Flood. Con gráficos impresionantes, una campaña épica y multijugador competitivo, Halo 3 es un clásico del Xbox 360.',
                'genero': 'shooter',
                'desarrolladora': 'Bungie',
                'ano_lanzamiento': 2007,
                'clasificacion': 'M',
                'precio': 29.99,
                'disponible': True,
            },
            {
                'titulo': 'Gears of War',
                'descripcion': 'Un shooter en tercera persona que revolucionó el género. Únete a Marcus Fenix y su escuadrón Delta en una guerra desesperada contra los Locust. Con mecánicas de combate innovadoras y gráficos de última generación.',
                'genero': 'shooter',
                'desarrolladora': 'Epic Games',
                'ano_lanzamiento': 2006,
                'clasificacion': 'M',
                'precio': 24.99,
                'disponible': True,
            },
            {
                'titulo': 'Mass Effect 2',
                'descripcion': 'Una épica aventura espacial donde tus decisiones importan. Como Comandante Shepard, reúne un equipo de élite para enfrentar una amenaza que podría destruir toda la galaxia. RPG de acción con narrativa profunda y combate táctico.',
                'genero': 'rpg',
                'desarrolladora': 'BioWare',
                'ano_lanzamiento': 2010,
                'clasificacion': 'M',
                'precio': 34.99,
                'disponible': True,
            },
            {
                'titulo': 'The Elder Scrolls V: Skyrim',
                'descripcion': 'Explora el vasto mundo de Skyrim como el Dovahkiin, el último de los Sangre de Dragón. Un RPG de mundo abierto con infinitas posibilidades, dragones, magia y aventuras épicas.',
                'genero': 'rpg',
                'desarrolladora': 'Bethesda Game Studios',
                'ano_lanzamiento': 2011,
                'clasificacion': 'M',
                'precio': 39.99,
                'disponible': True,
            },
            {
                'titulo': 'Call of Duty: Modern Warfare 2',
                'descripcion': 'La secuela del aclamado Modern Warfare. Combate en múltiples frentes con una campaña intensa y multijugador competitivo que definió una generación de shooters.',
                'genero': 'shooter',
                'desarrolladora': 'Infinity Ward',
                'ano_lanzamiento': 2009,
                'clasificacion': 'M',
                'precio': 27.99,
                'disponible': True,
            },
            {
                'titulo': 'Red Dead Redemption',
                'descripcion': 'Vive la épica historia del forajido John Marston en el salvaje oeste. Un mundo abierto lleno de aventuras, tiroteos y decisiones morales en una de las mejores experiencias del Xbox 360.',
                'genero': 'aventura',
                'desarrolladora': 'Rockstar Games',
                'ano_lanzamiento': 2010,
                'clasificacion': 'M',
                'precio': 32.99,
                'disponible': True,
            },
            {
                'titulo': 'Assassin\'s Creed II',
                'descripcion': 'Únete a Ezio Auditore en el Renacimiento italiano. Un juego de sigilo y acción con parkour, combate fluido y una historia intrigante sobre templarios y asesinos.',
                'genero': 'aventura',
                'desarrolladora': 'Ubisoft Montreal',
                'ano_lanzamiento': 2009,
                'clasificacion': 'M',
                'precio': 28.99,
                'disponible': True,
            },
            {
                'titulo': 'Forza Motorsport 3',
                'descripcion': 'La experiencia de conducción más realista del Xbox 360. Más de 400 coches, pistas icónicas y física de conducción avanzada. El simulador de carreras definitivo.',
                'genero': 'carreras',
                'desarrolladora': 'Turn 10 Studios',
                'ano_lanzamiento': 2009,
                'clasificacion': 'E',
                'precio': 26.99,
                'disponible': True,
            },
            {
                'titulo': 'FIFA 12',
                'descripcion': 'El fútbol más realista llega al Xbox 360. Con el nuevo Impact Engine, física mejorada y jugabilidad refinada. Disfruta del deporte rey con tus equipos favoritos.',
                'genero': 'deportes',
                'desarrolladora': 'EA Sports',
                'ano_lanzamiento': 2011,
                'clasificacion': 'E',
                'precio': 22.99,
                'disponible': True,
            },
            {
                'titulo': 'Batman: Arkham Asylum',
                'descripcion': 'Conviértete en el Caballero Oscuro en este juego de acción y sigilo. Combate fluido, acertijos desafiantes y una historia que captura la esencia de Batman.',
                'genero': 'accion',
                'desarrolladora': 'Rocksteady Studios',
                'ano_lanzamiento': 2009,
                'clasificacion': 'T',
                'precio': 25.99,
                'disponible': True,
            },
            {
                'titulo': 'BioShock',
                'descripcion': 'Explora la ciudad submarina de Rapture en este shooter de primera persona con elementos RPG. Una historia fascinante, poderes únicos y una atmósfera inolvidable.',
                'genero': 'shooter',
                'desarrolladora': '2K Boston',
                'ano_lanzamiento': 2007,
                'clasificacion': 'M',
                'precio': 23.99,
                'disponible': True,
            },
            {
                'titulo': 'Grand Theft Auto V',
                'descripcion': 'Vive tres historias entrelazadas en Los Santos. Robos épicos, mundo abierto masivo y multijugador online. Una de las experiencias más completas del Xbox 360.',
                'genero': 'accion',
                'desarrolladora': 'Rockstar North',
                'ano_lanzamiento': 2013,
                'clasificacion': 'M',
                'precio': 44.99,
                'disponible': True,
            },
            {
                'titulo': 'Dead Space',
                'descripcion': 'Terror en el espacio profundo. Como ingeniero Isaac Clarke, sobrevive a los horrores de la estación espacial USG Ishimura. Horror psicológico y combate estratégico.',
                'genero': 'terror',
                'desarrolladora': 'EA Redwood Shores',
                'ano_lanzamiento': 2008,
                'clasificacion': 'M',
                'precio': 24.99,
                'disponible': True,
            },
            {
                'titulo': 'Street Fighter IV',
                'descripcion': 'El regreso del rey de los juegos de lucha. Combate 2D con gráficos 3D, nuevos personajes y mecánicas clásicas mejoradas. La experiencia de lucha definitiva.',
                'genero': 'lucha',
                'desarrolladora': 'Capcom',
                'ano_lanzamiento': 2009,
                'clasificacion': 'T',
                'precio': 21.99,
                'disponible': True,
            },
            {
                'titulo': 'Portal 2',
                'descripcion': 'Resuelve acertijos ingeniosos con el Portal Gun. Una experiencia única de puzzle y plataformas con humor inteligente y mecánicas innovadoras.',
                'genero': 'plataformas',
                'desarrolladora': 'Valve Corporation',
                'ano_lanzamiento': 2011,
                'clasificacion': 'E10+',
                'precio': 19.99,
                'disponible': True,
            },
        ]

        self.stdout.write('Creando juegos de ejemplo...')
        
        for juego_data in juegos_ejemplo:
            juego, created = Juego.objects.get_or_create(
                titulo=juego_data['titulo'],
                defaults=juego_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'[OK] Creado: {juego.titulo}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'[--] Ya existe: {juego.titulo}')
                )
        
        total = Juego.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'\n¡Completado! Total de juegos en la base de datos: {total}')
        )

