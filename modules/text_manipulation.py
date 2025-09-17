#!/usr/bin/env python3

import unicodedata


#strip accents
def strip_accents(text):
    text = unicodedata.normalize('NFKD', text)
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn')

 #List of Puerto Rican slang words for filtering
puerto_rican_slang = [
    "Acho", "Wepa", "Chévere", "Nene", "Nena", "Boricua", "Janguear", "Guagua", "Corillo", "Chavo", "puto", "putos", "putas", "bicho", "regueton", "reggaeton", "bichote", "caco", "puta",
    "perra", "bellaco", "bellaca", "mamey", "zangano", "zangana", "chavo", "chava", "chavos", "chavas", 
    "perreo", "perrea", "cabrón", "Puerto", "rico", "Mofongo", "Brutal", "Pichea", "Fren", "Chinchorro",
    "Tato", "Nítido", "Bregar", "Al garete", "Jartera", "Ñangotarse", "Zafacón", "Gufear", "Mandilón",
    "Jibaro", "Cangri", "Jíbaro", "Guillao", "Tiguere", "Guilla", "Chombo", "Coro", "Chavos",
    "Vacilón", "Chota", "Chinchorreo", "To’", "Mamey", "Bayunco", "Naco", "Changuería",
    "La Jeva", "Chulear", "Ponte las pilas", "Estoy ready", "Tirar la toalla", "Pegar la vuelta",
    "Estar pelao", "Montar un coro", "Estar jarto", "En candela", "Hacer corillo", "La nota",
    "Arroz con habichuelas", "Me pica el bagre", "Chango", "La guagua", "Cotorra", "Chiviarse",
    "En bola", "Dar la talla", "Mabí", "Tiraera", "Tramar", "Guaguaeta", "Pichea eso", "Jeva",
    "Güevón", "Montar un palo", "Ronear", "Arroz con dulce", "To’ guilla", "Chacho", "Mangó", "A fuego",
    "Bregar con", "Mambo", "Pichear", "Chongo", "Tigre", "Mangú", "Güira", "Tumbao", "A la orden",
    "Chichaito", "Chivear", "Vacilar", "Pelea de gallos", "Changa", "La brega", "Tiradera", "Ponerse las pilas",
    "Guaraguao", "Majar", "Arrecho", "Pelar", "Chiripi", "Pelea de calle", "Tigueraje", "Chivo", "Pichar",
    "Rolo", "Bregar duro", "Chinchorrear", "Cangrim", "Brutalísimo", "Guay", "Mangú de plátano", "Chola",
    "Ñema", "Zafaconear", "Matar un tigre", "Bregar con la vida", "Jeva buena", "Chamaquita",
    "Mangú de guineo", "Guapo", "Vacilar duro", "Tiraera caliente", "Chinchorreo nocturno", "Bregando",
    "Pichear eso ya", "Mandilón perdido", "Jangueo", "Fular", "Ñangote", "Pajilla", "Chilindrón",
    "Zafacón lleno", "Brutalito", "Jíbaro de ciudad", "Pichea pana", "Fren en candela", "Tumbao duro",
    "Changa loca", "Mangú sucio", "Choto", "Corillo loco", "Ponte alante", "Chicha", "Gufiado",
    "Mandilonazo", "Ñengo", "Chango pelúo", "Pelea callejera", "Chévere brutal", "Bregar a lo bestia",
    "Vacilón total", "Tiguerazo", "Guillao loco", "Jartera mala", "Chavo duro", "Pichar duro",
    "Mamey de calle", "Ronear fuerte", "Brega dura", "Tiraera fuerte", "Chinchorro duro",
    "Pelea de gallos fuerte", "Mangú con to'", "Corillo fuerte", "Jeva loca", "Mandilón fuerte",
    "Ñangotazo", "Vacilar bien", "Brutal total", "Jíbaro duro", "Chévere total",
    "Guagua loca", "Chota fuerte", "Zafacón roto", "Bregar sin parar", "Tumbao fuerte", "Pichea duro",
    "Fren loco", "Chulo", "Mamey suave", "Bregando fuerte", "Mandilón loco", "Chinchorreo fuerte",
    "Jangueo fuerte", "Vacilón brutal", "Pelea de calle dura", "Corillo brutal", "Ñangote fuerte",
    "Ronear duro", "Guillao fuerte", "Tigueraje brutal", "Mangú duro", "Chacho loco", "Pichear fuerte",
    "Fula fuerte", "Jartera brut    al", "Chavo loco", "Brega brutal", "Mandilón total", "Zafacón fuerte",
    "Chinchorro brutal", "Tumbao total", "Brutal loco", "Pelea callejera brutal",
    "Corillo total", "Jeva brutal", "Jangueo total", "Ñangotazo fuerte", "Vacilar total", "Fren brutal",
    "Cholo", "Mangú brutal", "Pichear total", "Chavo total", "Bregar brutal", "Zafacón total",
    "Jíbaro total", "Tigueraje total", "Guillao total", "Ronear total", "Bregar total", "Chacho brutal",
    "Pelea brutal", "Vacilar brutal", "Jartera total", "Chinchorro total", "Tumbao brutal",
    "Brutal brutal", "Pelea de gallos brutal"
]