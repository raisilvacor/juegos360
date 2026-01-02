"""
Comando de gestión para importar juegos del índice de juegos
https://es-xbox360-rgh.wixsite.com/juegos/post/%C3%ADndice-de-juegos
"""
from django.core.management.base import BaseCommand
from tienda.models import Juego
from decimal import Decimal


class Command(BaseCommand):
    help = 'Importa juegos del índice de juegos con precio de 3000 pesos'

    def handle(self, *args, **options):
        # Lista completa de juegos del índice
        titulos_juegos = [
            'Ace Combat 6: Fires of Liberation',
            'Adventure Time 1',
            'Adventure Time 2',
            'Afro Samurai',
            'Airforce Delta Storm',
            'Alan Wake',
            'Alice: Madness Returns',
            'Alien Hominid: HD',
            'Alien: Isolation',
            'Aliens vs. Predator',
            'Alone in the Dark',
            'America´s Army: True Soldiers',
            'Amped: Freestyle snowboarding',
            'Angry Birds: Trilogy',
            'Angry Birds: Star Wars',
            'Arcana Heart 3',
            'Army of Two 1',
            'Army of Two 2: The 40th Day',
            'Army of Two 3: The Devil´s Cartel',
            'Assassin´s Creed 1',
            'Assassin´s Creed 2',
            'Assassin´s Creed 3',
            'Assassin´s Creed 4: Black Flag',
            'Assassin´s Creed: Brotherhood',
            'Assassin´s Creed: Revelations',
            'Assassin´s Creed: Rogue',
            'Asura´s Wrath',
            'Atari: Anthology',
            'ATV 2: Quad Power Racing',
            'Auto Modellista',
            'Avatar',
            'Avatar: The Burning Earth',
            'Back to the future',
            'Baja 1000',
            'Baja: Edge of Control',
            'Bakugan Battle Brawlers',
            'Baldur´s Gate: Dark Alliance 1',
            'Baldur´s Gate: Dark Alliance 2',
            'Band Hero',
            'Banjo Kazooie: Nuts and Bolts',
            'Banjo Tooie',
            'Barbie: Horse Adventures',
            'Barbie y sus Hermanas: Rescate de Cachorros',
            'Batman: Arkham Asylum',
            'Batman: Arkham City',
            'Batman: Begins',
            'Batman: Rise of Sin Tzu',
            'Battlefield 4',
            'Battlefield Bad: Company 1',
            'Battlefield Bad: Company 2',
            'Battlestations: Midway',
            'Battlestations: Pacific',
            'Battlestar: Galactica',
            'Bayonetta',
            'Bee Movie',
            'Ben 10: Omniverse 1',
            'Ben 10: Omniverse 2',
            'Beyond: Good & Evil HD Arcade',
            'Big Mutha: Truckers',
            'Binary Domain',
            'Bioshock 1',
            'Bioshock: Infinite',
            'Birds of Steel',
            'Blade 2',
            'Black',
            'BlackSite: Area 51',
            'Blades of Time',
            'Blazblue',
            'Blinx 1: The Time Sweeper',
            'Blinx 2: Master of Time and Space',
            'Blood Drive',
            'Bloodrayne 2',
            'Bloody Roar',
            'Blur',
            'BMX XXX',
            'Bob Esponja: El Héroe',
            'Bodycount',
            'Bolt',
            'Borderlands 1',
            'Borderlands 2',
            'Borderlands: The Pre-Sequel',
            'Brave',
            'Brink',
            'Brothers in Arms: Hell\'s Highway',
            'Brütal Legend',
            'Bully: Scholarship Edition',
            'Burnout 1',
            'Burnout 2: Point of Impact',
            'Burnout 3: Takedown',
            'Burnout: Revenge',
            'Call of Cthulhu: Dark Corners of the Earth',
            'Call of Duty 2',
            'Call of Duty 2: Big Red One',
            'Call of Duty 3',
            'Call of Duty 4: Modern Warfare',
            'Call of Duty: Advanced Warfare',
            'Call of Duty: Black Ops',
            'Call of Duty: Black Ops 1',
            'Call of Duty: Black Ops 2',
            'Call of Duty: Finest Hour',
            'Call of Duty: Ghosts',
            'Call of Duty: Modern Warfare 2',
            'Call of Duty: Modern Warfare 3',
            'Call of Duty: World at War',
            'Call of Juarez',
            'Call of Juarez: Bound in Blood',
            'Call of Juarez: The Cartel',
            'Capitán América: Super Soldado',
            'Cars 1',
            'Cars 2',
            'Cars 3: Motivado para Ganar',
            'Castle Crashers',
            'Castlevania: Curse of Darkness',
            'Castlevania: Harmony of Despair',
            'Castlevania: Lords of Shadow 1',
            'Castlevania: Lords of Shadow 2',
            'Catherine',
            'Child of Light',
            'Clash of the Titans',
            'Command & Conquer 3',
            'Commandos 2: Men of Courage',
            'Como Entrenar a tu Dragon 2',
            'Conker: Live & Reloaded',
            'Conflict Desert Storm',
            'Constantine',
            'Counter Strike',
            'Counter Strike: Global Offensive',
            'Crackdown 1',
            'Crackdown 2',
            'Crash Bandicoot: The Wrath of Cortex',
            'Crash: Guerra al Coco Maniáco',
            'Crash: Nitro Kart',
            'Crash: of the Titans',
            'Crash: Twinsanity',
            'Crazy Taxi',
            'Crimson Skies: High Road to Revenge',
            'Crouching Tiger Hidden Dragon',
            'Crysis 1',
            'Crysis 2',
            'Crysis 3',
            'Dance Central 1',
            'Dance Central 2',
            'Dance Central 3',
            'Dante´s Inferno',
            'Dark',
            'Dark Messiah: Might & Magic Elements',
            'Dark Sector',
            'Darksiders 1',
            'Darksiders 2',
            'Dark Souls 1',
            'Dark Souls 2: Scholar of the First Sin',
            'Dark Void',
            'Darkwatch',
            'Deadfall: Adventures',
            'Dead lsland',
            'Dead Island: Escape',
            'Dead Island: Riptide',
            'Dead or Alive 2: Ultimate',
            'Dead or Alive 3',
            'Dead or Alive 4',
            'Dead or Alive 5: Ultimate',
            'Dead or Alive: Xtreme 2',
            'Deadpool',
            'Dead Rising 2: Off the Record',
            'Dead Space 1',
            'Dead Space 2',
            'Dead Space 3',
            'Dead to Rights: Retribution',
            'Deadly Premonition',
            'De Blob 2',
            'Destroy All Humans: Path of Furon',
            'Deus Ex: Human Revolution',
            'Devil May Cry: HD Collection',
            'Diablo 3',
            'Digimon: Rumble Arena 2',
            'Dirt 2',
            'Dirt 3',
            'Dirt Showdown',
            'Dishonored',
            'Doom 1-2-3 BFG Edition',
            'Doom 3',
            'Doom 3: Resurrection of Evil',
            'Dragon Age 2',
            'Dragon Age: Inquisition',
            'Dragon Age: Origins Awakening',
            'Dragon Ball: Raging Blast 1',
            'Dragon Ball: Raging Blast 2',
            'Dragon Ball: Xenoverse',
            'Dragon Ball Z: Battle of Z',
            'Dragon Ball Z: Burst Limit',
            'Dragon Ball Z: Ultimate Tenkaichi',
            'Dragon´s Dogma',
            'Drake: of the 99 Dragons',
            'Dreamfall: The Longest Journey',
            'Driver 3',
            'Driver: San Francisco',
            'Duck Tales: Remastered',
            'Duke Nukem: Forever',
            'Dynasty Warriors 5',
            'Dynasty Warriors 6',
            'Dynasty Warriors 7',
            'Earth Defense Force: 2025',
            'Earth Worm Jim HD',
            'EA Sports: MMA',
            'El Chavo Kart',
            'El Increible Hulk',
            'El Origen de los Guardianes',
            'El Shaddai: Ascension of The Metatron',
            'Emuladores Parte 1',
            'Enemy Front',
            'Enemy Territory: Quake Wars',
            'Enslaved: Odyssey to the West',
            'Epic Mickey 2: El Poder de Dos',
            'Eragon',
            'Eschatos',
            'ESDLA: El Retorno del Rey',
            'ESDLA 2: La Batalla por la Tierra Media',
            'ESDLA: La Conquista',
            'ESDLA: La Guerra del Norte',
            'ESDLA: Shadow of Mordor',
            'ESPN: NFL 2K5',
            'Eternal Sonata',
            'Evil Dead: a Fistful of Boomstick',
            'Evil Dead: Regeneration',
            'F1: Race Stars',
            'Fable',
            'Fable: Anniversary',
            'Fable: The Lost Charpters',
            'Fable 2',
            'Fable 3',
            'Fallout 3',
            'Fallout: New Vegas',
            'Family Guy',
            'Fantastic Four: Rise of the Silver Surfer',
            'Far Cry 2',
            'Far Cry 3',
            'Far Cry 4',
            'Far Cry: Instincts',
            'Far Cry: Instincts Predator',
            'Farming Simulator',
            'Fast & Furious: Showdown',
            'Fatal Frame 1',
            'Fatal Frame 2: Crimson Butterfly',
            'Fatal Frame 3: The Tormented',
            'Fight Night Round 3',
            'Fight Night Round 4',
            'Final Fantasy XIII',
            'Final Fantasy XIII-2',
            'Final Fantasy XIII: Lightning Returns',
            'FlatOut: Ultimate Carnage',
            'Forza Horizon',
            'Forza Horizon 2',
            'Forza Motorsport 3',
            'Forza Motorsport 4',
            'Fracture',
            'Full Auto',
            'Fuse',
            'Fuzion Frenzy 2',
            'Game of Thrones',
            'Gears of War',
            'Gears of War 2',
            'Gears of War 3',
            'Gears of War: Judgment',
            'Ghost Recon: Advanced Warfighter',
            'Ghost Recon: Advanced Warfighter 2',
            'Ghostbusters: The Video Game',
            'G.I. Joe: The Rise of Cobra',
            'Godfather: The Game',
            'Golden Axe: Beast Rider',
            'Grand Theft Auto IV',
            'Grand Theft Auto V',
            'Guitar Hero 2',
            'Guitar Hero 3: Legends of Rock',
            'Guitar Hero 5',
            'Guitar Hero: Aerosmith',
            'Guitar Hero: Metallica',
            'Guitar Hero: Van Halen',
            'Guitar Hero: Warriors of Rock',
            'Guitar Hero: World Tour',
            'Gun',
            'Halo 3',
            'Halo 3: ODST',
            'Halo 4',
            'Halo: Combat Evolved Anniversary',
            'Halo: Reach',
            'Halo Wars',
            'Harry Potter: Years 1-4',
            'Harry Potter: Years 5-7',
            'Heavenly Sword',
            'Hitman: Absolution',
            'Hitman: Blood Money',
            'Homefront',
            'Hulk',
            'Hunted: The Demon\'s Forge',
            'I Am Alive',
            'Incredible Hulk: Ultimate Destruction',
            'Injustice: Gods Among Us',
            'Iron Man',
            'Iron Man 2',
            'Jade Empire',
            'James Bond 007: Blood Stone',
            'James Bond 007: Quantum of Solace',
            'Jaws: Ultimate Predator',
            'Jet Set Radio Future',
            'Jumper: Griffin\'s Story',
            'Jurassic Park: The Game',
            'Just Cause',
            'Just Cause 2',
            'Kameo: Elements of Power',
            'Kane & Lynch: Dead Men',
            'Kane & Lynch 2: Dog Days',
            'Killer Is Dead',
            'Killzone 2',
            'King Kong',
            'Kingdoms of Amalur: Reckoning',
            'L.A. Noire',
            'Left 4 Dead',
            'Left 4 Dead 2',
            'Lego Batman',
            'Lego Batman 2: DC Super Heroes',
            'Lego Harry Potter: Years 1-4',
            'Lego Harry Potter: Years 5-7',
            'Lego Indiana Jones: The Original Adventures',
            'Lego Indiana Jones 2: The Adventure Continues',
            'Lego Marvel Super Heroes',
            'Lego Star Wars: The Complete Saga',
            'Lego Star Wars III: The Clone Wars',
            'Lego The Lord of the Rings',
            'Lego The Hobbit',
            'Lego Pirates of the Caribbean',
            'Lego: The Movie Videogame',
            'Lollipop Chainsaw',
            'Lost Odyssey',
            'Lost Planet: Extreme Condition',
            'Lost Planet 2',
            'Lost Planet 3',
            'Mafia II',
            'Marvel Ultimate Alliance',
            'Marvel Ultimate Alliance 2',
            'Marvel vs Capcom 2: New Age of Heroes',
            'Max Payne 1',
            'Max Payne 2: The Fall of Max Payne',
            'Max Payne 3',
            'Medal of Honor',
            'Medal of Honor: European Assault',
            'Medal of Honor: Frontline',
            'Medal of Honor: Rising Sun',
            'Mega man: Anniversary Edition',
            'Mercenaries: Playground of Destruction',
            'Mercenaries 2: World in Flames',
            'Metal Gear Rising: Revengeance',
            'Metal Gear Solid: 2-3',
            'Metal Gear Solid 5: Ground Zeroes',
            'Metal Gear Solid: Peace Walker',
            'Metro: Last Light',
            'Michael Jackson: The Experience',
            'Midnight Club: Los Angeles',
            'Minecraft',
            'Minecraft: Story Mode',
            'MindJack',
            'Mini Ninjas',
            'MLB 2K13',
            'Monopoly Plus',
            'Monster High: New Ghoul in School',
            'Monster Jam',
            'Monsters vs Aliens',
            'Mortal Kombat 9',
            'Mortal Kombat: Armageddon',
            'Mortal Kombat: Deception',
            'Mortal Kombat: Shaolin Monks',
            'Mortal Kombat vs DC Universe',
            'Moto GP 2',
            'Moto GP 15',
            'MX Vs ATV: Untamed',
            'My Sims: Sky Heroes',
            'N3 Ninety Nine Nights 1',
            'N3 Ninety Nine Nights 2',
            'Nail´d',
            'Naruto: Rise of a Ninja',
            'Naruto: The Broken Bond',
            'Naruto Shippuden UN: Storm 2',
            'Naruto Shippuden UN: Storm 3',
            'Naruto Shippuden UN: Storm Generations',
            'Naruto Shippuden UN: Storm Revolution',
            'Nascar 15',
            'Naughty Bear',
            'Need for Speed: Carbon',
            'Need for Speed: Hot Pursuit',
            'Need for Speed: Most Wanted',
            'Need for Speed: Pro Street',
            'Need for Speed: Rivals',
            'Need for Speed: Shift 1',
            'Need for Speed: Shift 2 Unleashed',
            'Need for Speed: The Run',
            'Need for Speed: Undercover',
            'Need for Speed: Underground 1',
            'Need for Speed: Underground 2',
            'Neverdead',
            'NHL 15',
            'Nier',
            'Night at the Museum',
            'Nike: Kinect Training',
            'Ninja Blade',
            'Ninja Gaiden',
            'Ninja Gaiden Black',
            'Ninja Gaiden 2',
            'Ninja Gaiden 3: Razor´s Edge',
            'Ninja Gaiden Z Yaiba',
            'Operation Flashpoint; Dragon Rising',
            'Outlaw Tennis',
            'Overlord 1',
            'Overlord 2',
            'Pac-Man: World 3',
            'Pacman 2: y las Aventuras Fantasmales',
            'Panzer Dragoon: Orta',
            'Pay Day 2',
            'Peggle: Deluxe',
            'PES 14',
            'PES 15',
            'PES 16',
            'PES 17',
            'PES 18',
            'Phantom Dust',
            'Planet 51',
            'Plantas vs Zombies',
            'Playboy: The Mansion',
            'Portal',
            'Predator: Concrete Jungle',
            'Prince of Persia',
            'Principe de Persia 1: The Sands of Time',
            'Principe de Persia 2: Warrior Within',
            'Principe de Persia 3: Los Dos Tronos',
            'Prince of Persia: The Forgotten Sands',
            'Project Gotham Racing 4',
            'Prototype 1',
            'Prototype 2',
            'Rabbids: Alive & Kicking',
            'Rage',
            'RalliSport: Challenge 1',
            'RalliSport: Challenge 2',
            'Raskulls',
            'Ratatouille',
            'Rayman 1: Origins',
            'Rayman 2: Legends',
            'Rayman: Arena',
            'Rayman: Raving Rabbids',
            'Read Dead Redemption',
            'Red Faction Guerrilla',
            'Remember Me',
            'Resident Evil 4',
            'Resident Evil 5',
            'Resident Evil 6',
            'Resident Evil: Biohazard',
            'Resident Evil: Code Veronica X',
            'Resident Evil: Operation Raccoon City',
            'Resident Evil: Revelations',
            'Resident Evil: Revelations 2',
            'Resonance of Fate',
            'Ride',
            'Rio',
            'Rise of the Tomb Raider',
            'Rock Band: The Beatles',
            'Rocky',
            'Rocky: Legends',
            'Rugby 15',
            'Sacred 2: Fallen Angel',
            'Sacred 3',
            'Saints Row 1',
            'Saints Row 2',
            'Saints Row 4',
            'Saints Row: Gat Out of Hell',
            'Samurai Warriors',
            'Saw 2: Flesh & Blood',
            'SBK X: Superbike World Championship',
            'Scarface: The World is Yours',
            'Scooby Doo! Night of 100 Frights',
            'Serious Sam',
            'Shadows of the Damned',
            'Silent Hill HD Collection 2-3',
            'Silent Hill 4: The Room',
            'Singularity',
            'Skate 3',
            'Skullgirls',
            'Sleeping Dogs',
            'Sniper 2 Ghost Warrior',
            'Snoopys: Grand Adventure',
            'Sonic and Sega AllStars Racing',
            'Sonic Generations',
            'Sonic Transformed',
            'Sonic: Unleashed',
            'Sonic´s Ultimate Genesis Collection',
            'Soul Calibur 1',
            'Soul Calibur 2',
            'Soul Calibur 4',
            'Soul Calibur 5',
            'South Park: The Stick of Truth',
            'Spawn: Armageddon',
            'Spec Ops: The Line',
            'Speed Kings',
            'Spider Man 1',
            'Spider Man 2',
            'Spider Man 3',
            'Spider Man: Shattered Dimensions',
            'Spider Man: The Amazing',
            'Spiderman: Ultimate',
            'Spider Man: Web of Shadows',
            'Splatter House',
            'Splinter Cell: Blacklist',
            'Splinter Cell: Chaos Theory',
            'Splinter Cell: Double Agent',
            'Splinter Cell: Pandora Tomorrow',
            'Split Second',
            'SpongeBob: Battle for Bikini Bottom',
            'SpongeBob: Lights, Camera, Pants!',
            'SpongeBob: The Movie',
            'Spy Hunter 2',
            'Star Wars III: Revenge of the Sith',
            'Star Wars: Battlefront 1',
            'Star Wars: Battlefront 2',
            'Star Wars: El Poder de la Fuerza 2',
            'Star Wars Jedi Knight: Jedi Academy',
            'State of Decay',
            'Stormrise',
            'Street Fighter: Anniversary Collection',
            'Street Fighter 4 Ultra',
            'Street Fighter X Tekken',
            'Stubbs The Zombie: In Rebel Without a Pulse',
            'Supreme Commander',
            'Surf´s Up',
            'Syndicate',
            'Tales of Vesperia',
            'Taz: Wanted',
            'TC Ghost Recon 2',
            'TC Ghost Recon 2: Summit Strike',
            'TC Ghost Recon: Future Soldier',
            'TC Rainbow Six 3 Black Arrow',
            'TC Rainbow Six Vegas 1',
            'TC Rainbow Six Vegas 2',
            'Teenage Mutant Ninja Turtles',
            'Teenage Mutant Ninja Turtles: Mutans in Manhattan',
            'Tekken 6',
            'Tekken: Tag Tournament 2',
            'Test Drive Unlimited 2',
            'The Bureau: Xcom Declassified',
            'The Darkness 1',
            'The Darkness 2',
            'The Da Vinci Code',
            'The Elder Scrolls V: Skyrim',
            'The Evil Within',
            'The Godfather 1',
            'The Gunstringer',
            'The King of Fighters 12',
            'The King of Fighters 13',
            'The King of Fighters Neowave',
            'The Last Remnant',
            'The Sims 3',
            'The Wheelman',
            'The Witcher 2',
            'Thor: God of Thunder',
            'TNA Impact: Total Nonstop Action Wrestling',
            'Tomb Raider',
            'Tomb Raider Underworld',
            'Tony Hawk´s: American Wasteland',
            'Tony Hawk\'s: American Wasteland (Clásico)',
            'Tony Hawk´s: Pro Skater 5',
            'Tony Hawk´s: Proving Ground',
            'Too Human',
            'Top Spin 4',
            'Toy Story 3',
            'Toy Story Mania',
            'Transformers: El Lado Oscuro de la Luna',
            'Transformers: La Caída de Cybertron',
            'Transformers: Rise of the Dark Spark',
            'Tron Evolution',
            'Tropico 5',
            'Turning Point: Fall of Liberty',
            'Two Worlds',
            'Ultimate Marvel vs Capcom 3',
            'Unreal Championship 2',
            'Unreal Tournament 3',
            'UP',
            'Vanquish',
            'Velvet Assassin',
            'Venetica',
            'Vietcong Purple Haze',
            'Virtua Tennis 3',
            'Wall E',
            'Wanted: Weapons of Fate',
            'Warhammer 40000: Space Marine',
            'Watch Dogs',
            'Wolfenstein',
            'Wolfenstein: Return to Castle Tides of war',
            'Worms 4 Mayhem',
            'WRC 4: FIA World Rally Championship',
            'WRC 5',
            'WWE 2K14',
            'WWE 2K15',
            'WWE 2K16',
            'WWE All Stars',
            'Xcom: Enemy Unknown',
            'Xcom: Enemy Within',
            'XIII',
            'Xmen Origins: Wolverine',
            'Your Shape FE 2012',
            'Zumba: Fitness Core',
            'Zumba: Fitness Rush',
            '25 To Life',
        ]

        # Precio fijo: 3000 pesos
        precio_fijo = Decimal('3000.00')
        
        # Función para generar una URL de imagen genérica basada en el título
        def generar_url_imagen(titulo):
            # Limpiar el título para crear una URL
            titulo_limpio = titulo.lower().replace(' ', '-').replace(':', '').replace('\'', '').replace('´', '')
            titulo_limpio = ''.join(c for c in titulo_limpio if c.isalnum() or c == '-')
            # Retornar una URL genérica (puedes cambiar esto por una URL real de imágenes)
            return f'https://via.placeholder.com/400x600?text={titulo.replace(" ", "+")}'
        
        # Función para inferir género basado en palabras clave del título
        def inferir_genero(titulo):
            titulo_lower = titulo.lower()
            if any(palabra in titulo_lower for palabra in ['racing', 'speed', 'need for speed', 'forza', 'dirt', 'moto', 'nascar', 'wrc', 'cars', 'driver']):
                return 'carreras'
            elif any(palabra in titulo_lower for palabra in ['fifa', 'pes', 'nhl', 'mlb', 'nfl', 'rugby', 'sports', 'farming']):
                return 'deportes'
            elif any(palabra in titulo_lower for palabra in ['fighter', 'street fighter', 'tekken', 'mortal kombat', 'soul calibur', 'dead or alive', 'blazblue', 'king of fighters', 'marvel vs capcom']):
                return 'lucha'
            elif any(palabra in titulo_lower for palabra in ['horror', 'dead space', 'silent hill', 'resident evil', 'fatal frame', 'evil within', 'dark']):
                return 'terror'
            elif any(palabra in titulo_lower for palabra in ['call of duty', 'battlefield', 'halo', 'gears of war', 'medal of honor', 'ghost recon', 'rainbow six', 'counter strike', 'doom', 'wolfenstein', 'bioshock', 'crysis', 'far cry', 'sniper']):
                return 'shooter'
            elif any(palabra in titulo_lower for palabra in ['rpg', 'dragon age', 'mass effect', 'elder scrolls', 'fallout', 'fable', 'final fantasy', 'tales of', 'witcher', 'diablo', 'sacred', 'two worlds', 'kingdoms of amalur']):
                return 'rpg'
            elif any(palabra in titulo_lower for palabra in ['sonic', 'crash', 'banjo', 'rayman', 'spyro', 'lego', 'mario', 'platform']):
                return 'plataformas'
            elif any(palabra in titulo_lower for palabra in ['strategy', 'command & conquer', 'supreme commander', 'xcom']):
                return 'estrategia'
            else:
                return 'accion'  # Por defecto
        
        # Función para inferir desarrolladora común
        def inferir_desarrolladora(titulo):
            titulo_lower = titulo.lower()
            if 'halo' in titulo_lower:
                return 'Bungie / 343 Industries'
            elif 'gears of war' in titulo_lower:
                return 'Epic Games'
            elif 'assassin\'s creed' in titulo_lower or 'assassins creed' in titulo_lower:
                return 'Ubisoft'
            elif 'call of duty' in titulo_lower:
                return 'Infinity Ward / Treyarch'
            elif 'battlefield' in titulo_lower:
                return 'EA DICE'
            elif 'forza' in titulo_lower:
                return 'Turn 10 Studios'
            elif 'fifa' in titulo_lower or 'pes' in titulo_lower:
                return 'EA Sports / Konami'
            elif 'resident evil' in titulo_lower:
                return 'Capcom'
            elif 'final fantasy' in titulo_lower:
                return 'Square Enix'
            elif 'grand theft auto' in titulo_lower or 'gta' in titulo_lower:
                return 'Rockstar Games'
            elif 'elder scrolls' in titulo_lower or 'fallout' in titulo_lower:
                return 'Bethesda'
            elif 'lego' in titulo_lower:
                return 'Traveller\'s Tales'
            elif 'batman' in titulo_lower:
                return 'Rocksteady Studios'
            elif 'need for speed' in titulo_lower:
                return 'EA Black Box'
            else:
                return 'Varias Desarrolladoras'
        
        # Función para inferir año de lanzamiento (promedio para Xbox 360)
        def inferir_ano(titulo):
            # Intentar extraer año del título
            import re
            años_en_titulo = re.findall(r'\b(19|20)\d{2}\b', titulo)
            if años_en_titulo:
                año = int(años_en_titulo[0])
                if 2005 <= año <= 2016:
                    return año
            
            # Si no hay año, usar un año promedio basado en la serie
            titulo_lower = titulo.lower()
            if any(palabra in titulo_lower for palabra in ['halo 4', 'gears of war 3', 'assassin\'s creed 3', 'call of duty: black ops 2']):
                return 2012
            elif any(palabra in titulo_lower for palabra in ['halo 3', 'gears of war', 'assassin\'s creed 2', 'call of duty: modern warfare 2']):
                return 2009
            elif any(palabra in titulo_lower for palabra in ['halo reach', 'gears of war 2']):
                return 2010
            else:
                return 2010  # Año promedio
        
        # Función para inferir clasificación
        def inferir_clasificacion(titulo):
            titulo_lower = titulo.lower()
            if any(palabra in titulo_lower for palabra in ['call of duty', 'gears of war', 'halo', 'bioshock', 'dead space', 'resident evil', 'silent hill', 'gta', 'grand theft auto', 'max payne', 'dead rising', 'darksiders', 'prototype', 'saints row', 'mortal kombat', 'dead or alive: xtreme']):
                return 'M'
            elif any(palabra in titulo_lower for palabra in ['batman', 'assassin\'s creed', 'tomb raider', 'splinter cell', 'hitman', 'sleeping dogs', 'watch dogs']):
                return 'T'
            elif any(palabra in titulo_lower for palabra in ['lego', 'sonic', 'crash', 'rayman', 'spyro', 'cars', 'toy story', 'spongebob', 'ben 10', 'adventure time']):
                return 'E'
            else:
                return 'T'  # Por defecto
        
        self.stdout.write('Importando juegos del índice...')
        self.stdout.write(f'Total de juegos a importar: {len(titulos_juegos)}')
        
        creados = 0
        existentes = 0
        
        for titulo in titulos_juegos:
            # Crear descripción genérica
            descripcion = f'Juego de Xbox 360: {titulo}. Disponible para descarga inmediata después del pago.'
            
            juego_data = {
                'titulo': titulo,
                'descripcion': descripcion,
                'genero': inferir_genero(titulo),
                'desarrolladora': inferir_desarrolladora(titulo),
                'ano_lanzamiento': inferir_ano(titulo),
                'clasificacion': inferir_clasificacion(titulo),
                'precio': precio_fijo,
                'imagen': generar_url_imagen(titulo),
                'disponible': True,
            }
            
            juego, created = Juego.objects.get_or_create(
                titulo=titulo,
                defaults=juego_data
            )
            
            if created:
                creados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'[OK] Creado: {titulo}')
                )
            else:
                existentes += 1
                # Actualizar precio si el juego ya existe
                if juego.precio != precio_fijo:
                    juego.precio = precio_fijo
                    juego.save()
                    self.stdout.write(
                        self.style.WARNING(f'[$$] Actualizado precio: {titulo}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'[--] Ya existe: {titulo}')
                    )
        
        total = Juego.objects.count()
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(f'¡Completado!')
        )
        self.stdout.write(f'  - Juegos creados: {creados}')
        self.stdout.write(f'  - Juegos existentes: {existentes}')
        self.stdout.write(f'  - Total de juegos en la base de datos: {total}')

