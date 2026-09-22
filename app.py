import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64

# ============================================================
# PAGE CONFIG — must be the first Streamlit command
# ============================================================
st.set_page_config(
    page_title="Britney's Kids in Wonderland Book 1",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CUSTOM CSS — Golden book style + big header
# ============================================================
st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(900px 500px at 50% -10%, rgba(58,160,255,.18), transparent 65%),
            radial-gradient(700px 500px at 10% 110%, rgba(255,217,59,.08), transparent 60%),
            radial-gradient(700px 500px at 90% 110%, rgba(58,160,255,.10), transparent 60%),
            #0a0e1a;
    }
    .main-title {
        font-family: 'Georgia', serif;
        font-size: clamp(1.6rem, 5vw, 3rem);
        font-weight: 900;
        letter-spacing: 3px;
        text-align: center;
        background: linear-gradient(90deg, #ffd93b 0%, #ff9f00 50%, #c8811a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 6px;
        text-shadow: 0 0 40px rgba(255,159,0,.35);
    }
    .be-like-brit {
        font-family: 'Georgia', serif;
        font-size: clamp(.85rem, 2vw, 1.15rem);
        font-weight: 900;
        letter-spacing: 4px;
        color: #3aa0ff;
        text-align: center;
        text-transform: uppercase;
        text-shadow: 0 0 16px rgba(58,160,255,.85), 0 0 34px rgba(58,160,255,.55);
        margin-bottom: 4px;
    }
    .book-sub {
        font-size: clamp(.75rem, 1.5vw, .95rem);
        font-weight: 800;
        letter-spacing: 3px;
        color: #8fa9d1;
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .author-name {
        font-family: 'Georgia', serif;
        font-size: clamp(.95rem, 2.2vw, 1.3rem);
        font-weight: 900;
        letter-spacing: 2px;
        color: #ffd93b;
        text-align: center;
        text-shadow: 0 0 20px rgba(255,217,59,.75);
    }
    .author-role {
        font-size: clamp(.65rem, 1.3vw, .8rem);
        letter-spacing: 3px;
        color: #8fa9d1;
        text-align: center;
        text-transform: uppercase;
        font-weight: 900;
        margin-bottom: 6px;
    }
    .contact-row {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 12px;
        font-size: clamp(.78rem, 1.4vw, .95rem);
        font-weight: 900;
        margin-bottom: 12px;
    }
    .contact-row span {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 18px;
        border-radius: 999px;
        background: rgba(255,217,59,.15);
        border: 2px solid rgba(255,217,59,.55);
        color: #ffe680;
        box-shadow: 0 0 20px rgba(255,217,59,.20);
    }
    .contact-row a {
        color: #ffd93b;
        text-decoration: none;
        font-weight: 900;
        border-bottom: 1px dotted rgba(255,217,59,.7);
    }
    .page-title {
        font-family: 'Georgia', serif;
        font-size: clamp(1.1rem, 2.6vw, 1.7rem);
        font-weight: 900;
        color: #3a2208;
        text-align: center;
        margin-bottom: 12px;
    }
    .page-text {
        font-family: 'Georgia', serif;
        font-size: clamp(.98rem, 2vw, 1.2rem);
        line-height: 1.85;
        color: #2a1a08;
        text-align: center;
        padding: 8px 6px;
        letter-spacing: .3px;
    }
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 900 !important;
        letter-spacing: 1.2px !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stAudio"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# BOOK CONTENT — 100 pages
# ============================================================
PAGES = [
    # ---------- 1–10 : IMPORTANCE OF ENGLISH ----------
    {"title": "Hello, English!", "text": "English is a gift that opens doors all over the world. When you learn English, you can talk to children in America, Africa, Europe and Asia. You can read stories, sing songs, and make new friends. English is not hard when you learn it one word at a time. Today, let us start with a smile and say: Hello, English!"},
    {"title": "Words Are Magic Keys", "text": "Every English word is a magic key. One key opens a book. Another key opens a song. Another key opens a friendship. The more words you learn, the more doors you can open. So learn one new word every day. Soon, you will have a whole ring of magic keys."},
    {"title": "Why English Is Fun", "text": "English is fun because it is full of sounds! The letter S sings like a snake. The letter B bounces like a ball. The letter M hums like a happy mother. When you play with sounds, English becomes a game. And games are always fun to win."},
    {"title": "The English Garden", "text": "Imagine a garden where every flower is an English word. Red roses are verbs. Yellow daisies are nouns. Blue bells are adjectives. When you walk in this garden, you pick words and put them in your basket. Soon your basket is full, and you can make beautiful sentences."},
    {"title": "English Helps You Dream", "text": "When you know English, you can dream in two languages. You can dream of castles in France and rockets in America. You can dream of oceans and mountains and stars. English does not limit your dreams. It makes them bigger."},
    {"title": "Speak with Confidence", "text": "Do not be afraid to speak English. Every great speaker started with one word. Speak slowly. Speak clearly. If you make a mistake, smile and try again. The more you speak, the easier it becomes. Your voice is beautiful in any language."},
    {"title": "English Is a Bridge", "text": "English is a bridge between people. On one side is your home, your family, your language. On the other side is the whole world. When you learn English, you build that bridge. You can walk across it whenever you want. You can meet anyone, anywhere."},
    {"title": "The First English Lesson", "text": "On the first day of English class, a little girl named Britney raised her hand. She said, 'Teacher, I only know two words.' The teacher smiled and said, 'Two words are enough to start. Tomorrow you will know four. Next week, twenty. Next year, a thousand.' Britney smiled. She knew she could do it."},
    {"title": "Read, Read, Read", "text": "The best way to learn English is to read. Read signs. Read labels. Read stories. Read poems. Read everything you can find. Every sentence you read teaches your brain a new pattern. Soon, English will feel like home."},
    {"title": "You Can Do It", "text": "Learning English is like climbing a mountain. Some days are easy. Some days are hard. But every step takes you higher. And when you reach the top, you will see the whole world below you. You can do it. One word, one step, one day at a time."},

    # ---------- 11–20 : THE FOREST ----------
    {"title": "The Whispering Forest", "text": "Deep in the whispering forest, the trees talk to each other. The old oak says, 'Good morning.' The pine says, 'Good morning.' The birch says, 'Good morning.' And all the little leaves clap their hands. If you are very quiet, you can hear them too."},
    {"title": "The Forest at Night", "text": "When the sun goes down, the forest changes. Fireflies light up like tiny stars. Owls wake up and say, 'Whoo.' The moon shines through the branches. The forest at night is a magical place, full of soft sounds and silver light."},
    {"title": "The Brave Little Squirrel", "text": "A little squirrel named Nutty lived in a tall tree. One day, a big storm came. Nutty was scared. But his mother said, 'Hold on tight, little one.' Nutty held on. When the storm passed, the sun came out, and Nutty was proud. He had been brave."},
    {"title": "The Secret Path", "text": "Behind the big rock, there is a secret path. Only the rabbits know it. It leads to a clearing where the grass is soft and the flowers are blue. If you follow the path quietly, you will find the secret place. But you must promise not to tell anyone."},
    {"title": "The Old Tree's Story", "text": "The oldest tree in the forest is three hundred years old. It has seen kings and queens. It has seen wars and peace. It has seen children grow up and have children of their own. If you sit under it, it will tell you stories. You only have to listen."},
    {"title": "The Forest River", "text": "A river runs through the forest. It is cold and clear. The fish swim in it. The deer drink from it. The birds bathe in it. The river says, 'I give water to everyone.' And everyone says, 'Thank you, river.'"},
    {"title": "The Friendly Fox", "text": "A friendly fox lived near the forest edge. He had a red coat and a white-tipped tail. Every morning, he visited his friends: the rabbit, the hedgehog, and the little mouse. 'Good morning, friends,' he said. And they all smiled."},
    {"title": "The Mushroom Village", "text": "Under a big log, there is a village of mushrooms. Red ones with white spots. Brown ones with flat caps. Tiny ones with long stems. They are all friends. They grow together, they dance together, they sleep together. The mushroom village is a happy place."},
    {"title": "The Forest in Spring", "text": "In spring, the forest wakes up. The snow melts. The buds open. The birds return. The bees buzz. Everything is green and new. The forest says, 'Spring is here!' And all the animals cheer."},
    {"title": "The Forest in Winter", "text": "In winter, the forest sleeps. The trees are bare. The ground is white. The animals hide in their warm homes. But even in winter, there is beauty. The snow sparkles. The air is fresh. The forest is resting, waiting for spring."},

    # ---------- 21–30 : FRIENDSHIP ----------
    {"title": "A Friend Is a Treasure", "text": "A friend is more precious than gold. Gold can be lost, but a true friend stays. A friend listens when you are sad. A friend laughs when you are happy. A friend helps when you are stuck. If you have a friend, you have everything."},
    {"title": "The Two Little Birds", "text": "Two little birds sat on a branch. One was blue. One was yellow. 'I am hungry,' said Blue. 'I will share my seeds,' said Yellow. They ate together. They sang together. They flew together. They were best friends."},
    {"title": "How to Make a Friend", "text": "To make a friend, you need three things: a smile, a kind word, and a listening ear. Smile first. Say hello. Ask a question. Listen to the answer. That is all. Friendship starts with one small step."},
    {"title": "The Lion and the Mouse", "text": "A big lion caught a tiny mouse. 'Please let me go,' said the mouse. 'One day I will help you.' The lion laughed, but he let the mouse go. Later, the lion was caught in a net. The mouse came and chewed the ropes. The lion was free. Friends come in all sizes."},
    {"title": "The Kindness Club", "text": "In a small school, some children started a Kindness Club. Every day, they did one kind thing: they helped a friend, shared a snack, or gave a compliment. Soon, the whole school was kind. Kindness spreads like sunshine."},
    {"title": "A Friend in the Rain", "text": "One rainy day, a little boy forgot his umbrella. He stood under a tree, sad. Then a girl came with her umbrella. 'Come under mine,' she said. They walked home together. The rain did not matter anymore. Friendship is warmer than sunshine."},
    {"title": "The Best Gift", "text": "On her birthday, Britney got many gifts: toys, books, and candies. But the best gift was a card from her friend. It said, 'You are my best friend.' Britney smiled. She knew that friendship was the best gift of all."},
    {"title": "Saying Sorry", "text": "Everyone makes mistakes. The brave thing is to say sorry. When you say sorry, you open the door for friendship to grow again. A simple 'I am sorry' can heal a heart."},
    {"title": "The Long Walk Home", "text": "Two friends walked home from school. The road was long. But they talked and laughed, and the road felt short. That is what friends do: they make hard things easy and long things short."},
    {"title": "Friends Forever", "text": "Friends may move away. Friends may grow up. But true friendship never ends. It lives in the heart. And when you meet again, it feels like no time has passed at all."},

    # ---------- 31–40 : FOOD TECHNOLOGY ----------
    {"title": "Food from the Future", "text": "Long ago, people cooked food on open fires. Today, we use ovens, microwaves, and smart pots. Tomorrow, food technology will be even more amazing. We will grow food in space. We will print food with 3D printers. The future of food is full of surprises."},
    {"title": "The Magic Fridge", "text": "A magic fridge knows what you need. It tells you when milk is old. It suggests recipes. It orders food online. The magic fridge is not a dream — it is already here. Technology makes our kitchens smarter every day."},
    {"title": "How Bread Is Made", "text": "Bread starts as a tiny seed of wheat. The seed grows into a plant. The plant becomes flour. The flour becomes dough. The dough is baked in an oven. And then, warm and golden, it becomes bread. Every loaf is a miracle."},
    {"title": "The Chocolate Story", "text": "Chocolate comes from a tree called cacao. The seeds are dried, roasted, and ground. Then sugar and milk are added. The mixture is shaped into bars. Chocolate is one of the most loved foods in the world. Thank you, cacao tree!"},
    {"title": "Fruits of the World", "text": "In Haiti, we eat mangoes. In Japan, they eat persimmons. In India, they eat guavas. In Brazil, they eat papayas. The world is full of delicious fruits. Every country has a special taste."},
    {"title": "The Healthy Plate", "text": "A healthy plate has many colors. Green vegetables. Red tomatoes. Yellow corn. Brown rice. White fish. When you eat many colors, your body gets many vitamins. Colorful food is happy food."},
    {"title": "Water Is Life", "text": "Clean water is the most important food of all. Without water, we cannot live. Water helps us grow, think, and play. Drink water every day. It is the simplest and best drink in the world."},
    {"title": "The Kitchen Science", "text": "Cooking is science. When you boil an egg, the protein changes. When you bake a cake, the batter rises. When you freeze water, it becomes ice. Every meal is a science experiment. And you are the scientist."},
    {"title": "Food from the Garden", "text": "The best food comes from your own garden. You plant a seed. You water it. You wait. Then one day, you pick a tomato or a pepper or a carrot. And it tastes better than anything you can buy. Growing food is magic."},
    {"title": "Sharing a Meal", "text": "Food tastes better when shared. When you eat alone, the meal is quiet. When you eat with family or friends, the meal is happy. Sharing a meal is sharing love."},

    # ---------- 41–50 : THE LITTLE PRINCESS ----------
    {"title": "The Little Princess", "text": "Once upon a time, there was a little princess named Amara. She lived in a castle on a hill. She had a golden crown and a kind heart. But she was not happy, because she had no friends. One day, she went outside the castle and met a village girl. They played together. And the princess learned that friendship is better than any crown."},
    {"title": "The Princess and the Star", "text": "Every night, the little princess looked at the stars. 'I wish I could touch one,' she said. One night, a star fell from the sky and landed in her garden. It was a tiny star, still shining. The princess held it gently. 'I will keep you safe,' she said. And the star shone brighter than ever."},
    {"title": "The Princess's Garden", "text": "The little princess loved her garden. She grew roses, lilies, and sunflowers. She talked to the flowers every morning. 'Good morning, roses. Good morning, lilies.' And the flowers grew taller and brighter, because they were loved."},
    {"title": "The Princess and the Frog", "text": "One day, the little princess found a frog in her pond. 'Hello, frog,' she said. The frog said, 'Hello, princess.' She was surprised! The frog could talk. They became friends. And every day, they sat by the pond and told stories."},
    {"title": "The Brave Princess", "text": "A dragon came to the kingdom. Everyone was afraid. But the little princess was not afraid. She walked to the dragon and said, 'Why are you here?' The dragon said, 'I am lonely.' The princess smiled. 'Then come and live with us.' And the dragon became the kindest friend in the castle."},
    {"title": "The Princess and the Poor Boy", "text": "The princess met a poor boy in the village. He had no shoes. She gave him hers. He had no food. She gave him hers. He had no home. She gave him a room in the castle. The boy grew up to be a great knight. And he never forgot her kindness."},
    {"title": "The Princess Who Loved Books", "text": "The little princess loved books more than jewels. She read stories about faraway lands, brave heroes, and magical creatures. 'Books are my treasure,' she said. And she was right."},
    {"title": "The Princess's Wish", "text": "One night, the princess saw a shooting star. 'I wish for peace in the world,' she said. And from that night, she worked every day to make peace real. She shared, she forgave, she loved. And peace grew in her kingdom."},
    {"title": "The Princess's Crown", "text": "The princess had a golden crown. But one day, she gave it to a poor girl. 'You are a princess too,' she said. 'Every girl is.' The poor girl smiled. And the princess felt richer than ever."},
    {"title": "The Princess's Lesson", "text": "The princess learned a great lesson: being a princess is not about a crown. It is about a kind heart. Anyone can be a princess. Anyone can be a king. It is not about what you wear. It is about who you are."},

    # ---------- 51–60 : THE TITLE BOY & TITLE PRINCE ----------
    {"title": "The Title Boy", "text": "Once, there was a boy who had no title. He was not a prince. He was not a knight. But he had a dream. Every day, he worked hard. Every night, he studied. Years passed. And one day, the king said, 'You are the bravest boy in the land. I give you a title.' And the boy became a hero."},
    {"title": "The Title Prince", "text": "The title prince was born in a palace. He had everything: gold, jewels, servants. But he was not happy. One day, he left the palace and walked into the forest. There, he met a poor family. He helped them build a house. And for the first time, he felt joy. He learned that true titles are earned, not given."},
    {"title": "The Boy Who Became King", "text": "A poor boy once found a wounded bird. He nursed it back to health. The bird was magical. It said, 'Because you are kind, you will one day be king.' Years later, the boy grew up. He became a wise and just king. And he never forgot the bird."},
    {"title": "The Prince's Journey", "text": "The young prince left his castle to see the world. He crossed rivers. He climbed mountains. He met people from many lands. When he returned, he was not the same. He was wiser, kinder, and braver. The journey had made him a true prince."},
    {"title": "The Title of Honor", "text": "There is a title greater than prince or king. It is the title of 'good person.' Anyone can earn it. You earn it by being honest. You earn it by being kind. You earn it by helping others. And once you have it, no one can take it away."},
    {"title": "The Boy with the Golden Heart", "text": "People said the boy had a golden heart. He shared his bread. He helped the old. He played with the lonely. Everyone loved him. And one day, the queen said, 'You are the richest boy in the kingdom, because your heart is made of gold.'"},
    {"title": "The Prince and the Servant", "text": "The prince and the servant were best friends. They played together, ate together, laughed together. The king was angry. 'A prince cannot be friends with a servant.' But the prince said, 'A heart does not care about titles.' And the king understood."},
    {"title": "The Prince's Promise", "text": "The prince promised to protect his people. He promised to be just. He promised to be kind. And he kept his promises every day of his life. That is what makes a true prince."},
    {"title": "The Boy Who Loved the Moon", "text": "A boy loved the moon. Every night, he watched it. 'One day, I will touch you,' he said. He studied. He learned. He built a rocket. And one day, he flew to the moon. He touched it. The moon was cold, but the boy was happy."},
    {"title": "The Title You Give Yourself", "text": "The greatest title is the one you give yourself. 'I am brave.' 'I am kind.' 'I am strong.' Say these words every day. Believe them. Live them. And the world will believe them too."},

    # ---------- 61–70 : KIDS STORIES IN GENERAL ----------
    {"title": "The Lost Kitten", "text": "A little kitten was lost in the rain. She meowed and meowed. A girl heard her and came running. She picked up the kitten and held her close. 'Do not be afraid,' she said. 'I will take you home.' And the kitten purred. She was safe."},
    {"title": "The Rainbow After the Storm", "text": "After a big storm, the sky cleared. And there, in the sky, was a rainbow. Red, orange, yellow, green, blue, indigo, violet. The children ran outside to see it. 'It is beautiful!' they said. And they knew that after every storm, there is a rainbow."},
    {"title": "The Butterfly's Journey", "text": "A caterpillar crawled on a leaf. 'I am slow,' she said. 'I will never fly.' But one day, she wrapped herself in a cocoon. She slept. And when she woke up, she had wings. She was a butterfly. She flew high in the sky. 'I can fly!' she said. Never give up on your dreams."},
    {"title": "The Boy and the Starfish", "text": "A boy walked on the beach. He saw many starfish on the sand. He picked one up and threw it into the sea. A man said, 'There are thousands. You cannot save them all.' The boy picked up another starfish. 'I saved this one,' he said. And he threw it into the sea."},
    {"title": "The Talking Tree", "text": "A tree in the park could talk. But only to children. 'Hello, little one,' said the tree. 'Hello, tree,' said the child. They talked about the birds, the wind, and the sun. The tree told stories. The child listened. And the tree was happy."},
    {"title": "The Little Star", "text": "A little star looked down at the earth. 'I am so small,' she said. 'I cannot do anything.' But one night, a sailor lost at sea saw her light. He followed it home. The little star smiled. Even a small light can save a life."},
    {"title": "The Secret Door", "text": "In the old library, there was a secret door. Only the librarian knew about it. One day, a curious girl found it. She opened it. Inside was a room full of books. 'These are the books that were never read,' said the librarian. 'Read them.' And the girl read every one."},
    {"title": "The Boy Who Could Fly", "text": "A boy dreamed he could fly. Every night, he flew over mountains and oceans. He saw the world from above. And when he woke up, he remembered the feeling. 'One day,' he said, 'I will fly for real.' And he did — in an airplane."},
    {"title": "The Kind Giant", "text": "A giant lived in the mountains. Everyone was afraid of him. But one day, a little girl fell and hurt her knee. The giant picked her up gently and carried her home. 'Thank you, giant,' she said. And the giant smiled. He was kind, not scary."},
    {"title": "The Magic Paintbrush", "text": "A girl found a magic paintbrush. Whatever she painted came to life. She painted a garden. Flowers grew. She painted a river. Water flowed. She painted a friend. And the friend smiled. 'Use your gift for good,' said the brush. And she did."},

    # ---------- 71–80 : NATURE & ANIMALS ----------
    {"title": "The Elephant's Memory", "text": "An elephant never forgets. He remembers every friend, every place, every kindness. Elephants are gentle giants. They walk slowly, they care for their families, they mourn their dead. They are among the wisest animals on earth."},
    {"title": "The Dolphin's Song", "text": "Dolphins sing to each other under the sea. They jump and play in the waves. They are smart and friendly. They help lost swimmers. They are the clowns of the ocean."},
    {"title": "The Penguin Parade", "text": "In the cold Antarctic, penguins walk in a line. One after another, they march to the sea. They dive and swim. They catch fish. Then they walk back, full and happy. The penguin parade is one of nature's wonders."},
    {"title": "The Turtle and the Hare", "text": "The hare was fast. The turtle was slow. 'I will win the race,' said the hare. He ran fast, then stopped to rest. The turtle walked slowly, never stopping. And the turtle won. Slow and steady wins the race."},
    {"title": "The Busy Bee", "text": "A little bee flew from flower to flower. She collected nectar. She made honey. She helped the flowers grow. 'I am busy,' she said. 'But I am happy.' Bees are small, but they do big things."},
    {"title": "The Whale's Journey", "text": "A great whale swam across the ocean. She sang her song. She visited cold waters and warm waters. She saw ships and islands and stars. The whale is the largest animal on earth. And she is gentle."},
    {"title": "The Rainforest", "text": "The rainforest is full of life. Monkeys swing in the trees. Parrots fly in the sky. Jaguars walk on the ground. Frogs croak in the ponds. Millions of species live together. The rainforest is a treasure."},
    {"title": "The Desert Flower", "text": "In the desert, a tiny flower grew. She had no water for many days. But she held on. And one day, the rain came. She opened her petals and bloomed. Even in the hardest place, life finds a way."},
    {"title": "The Mountain Peak", "text": "A mountain peak stands tall. Snow covers her head. Clouds wrap around her shoulders. She has been there for millions of years. She watches the world below. She is patient and strong."},
    {"title": "The Ocean's Song", "text": "The ocean sings a song. Waves crash on the shore. Seagulls cry in the wind. Fish swim in the deep. The ocean is full of music. Sit by the sea and listen."},

    # ---------- 81–90 : LIFE LESSONS FOR KIDS ----------
    {"title": "Be Brave, Little One", "text": "Being brave does not mean having no fear. It means doing what is right even when you are afraid. Be brave, little one. The world needs your courage."},
    {"title": "Always Say Thank You", "text": "Two words change everything: 'Thank you.' Say them to your mother. Say them to your teacher. Say them to the friend who helped you. Thank you is a small phrase with a big heart."},
    {"title": "Share Your Smile", "text": "Your smile is free, but it is worth a million dollars. When you smile at someone, you give them a gift. And smiles are contagious. Share your smile today."},
    {"title": "Learn from Mistakes", "text": "Mistakes are not bad. Mistakes are teachers. When you make a mistake, ask: 'What can I learn?' Then try again. And again. And again. That is how you grow."},
    {"title": "Be Kind to Everyone", "text": "Be kind to the rich. Be kind to the poor. Be kind to the happy. Be kind to the sad. Be kind to everyone. Kindness is the language that everyone understands."},
    {"title": "Dream Big", "text": "Do not dream small dreams. Dream big dreams. Dream of changing the world. Dream of helping others. Dream of being great. Because big dreams create big people."},
    {"title": "Never Give Up", "text": "When things get hard, do not give up. Take a deep breath. Rest. Then try again. Winners are not people who never fail. Winners are people who never quit."},
    {"title": "Love Your Family", "text": "Your family is your first team. They love you. They support you. They are always there. Love them back. Say 'I love you' often. Family is forever."},
    {"title": "Take Care of Your Body", "text": "Your body is your home. Eat healthy food. Drink water. Move. Sleep. Rest. When you take care of your body, it takes care of you."},
    {"title": "Be Yourself", "text": "You do not need to be like anyone else. You are unique. You are special. You are you. And that is more than enough."},

    # ---------- 91–100 : THE WONDERLAND FINALE ----------
    {"title": "Welcome to Wonderland", "text": "Welcome to Wonderland, dear reader. This is a place where imagination lives. Here, animals talk, stars sing, and dreams come true. You have arrived. And now the adventure begins."},
    {"title": "The Wonderland Garden", "text": "In Wonderland, there is a garden that never stops blooming. Roses of every color. Trees that grow candy. Rivers of honey. This is the garden of your dreams. You are welcome here."},
    {"title": "The Queen of Wonderland", "text": "The Queen of Wonderland is kind. She smiles at everyone. She helps everyone. She loves everyone. 'In Wonderland,' she says, 'we are all family.' And it is true."},
    {"title": "The Wonderland Friends", "text": "In Wonderland, you will meet many friends. The white rabbit. The talking cat. The smiling caterpillar. The dancing butterfly. They are all waiting for you. Come and play."},
    {"title": "The Wonderland Sky", "text": "The sky in Wonderland is always blue. The sun always shines. The stars always sparkle. The moon always smiles. It is a place of endless happiness."},
    {"title": "The Wonderland Story", "text": "Every child who visits Wonderland gets to write their own story. What will your story be? A princess? A knight? A hero? The choice is yours. Write it well."},
    {"title": "The Wonderland Promise", "text": "Before you leave Wonderland, remember this promise: 'I am brave. I am kind. I am loved. I am enough.' Say it every day. And Wonderland will live in your heart forever."},
    {"title": "The Return Home", "text": "You have traveled through Wonderland. You have met friends. You have learned lessons. Now it is time to go home. But Wonderland will always be with you. Close your eyes and you will see it again."},
    {"title": "Thank You, Reader", "text": "Thank you for reading this book. You have been a wonderful reader. You have learned. You have dreamed. You have grown. Now go out and share your light with the world."},
    {"title": "The End of Book One", "text": "This is the end of Book One. But the story does not end here. There are many more adventures to come. Book Two is waiting. Turn the page, and the wonder continues."},
]

# Ensure exactly 100 pages (pad if necessary)
while len(PAGES) < 100:
    PAGES.append({
        "title": f"Bonus Page {len(PAGES) + 1}",
        "text": "This is a bonus page of kindness and wonder. Read it, smile, and share it with a friend."
    })

# ============================================================
# SESSION STATE — track the current page
# ============================================================
if "page_index" not in st.session_state:
    st.session_state.page_index = 0

# ============================================================
# HEADER — big title, name, contact
# ============================================================
st.markdown('<div class="be-like-brit">BE LIKE BRIT</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">BRITNEY\'S KIDS IN WONDERLAND BOOK 1</div>', unsafe_allow_html=True)
st.markdown('<div class="book-sub">100 Pages · Read Aloud · Learn & Dream</div>', unsafe_allow_html=True)
st.markdown('<div class="author-name">BUILT BY GESNER DESLANDES</div>', unsafe_allow_html=True)
st.markdown('<div class="author-role">Technology Coordinator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="contact-row">'
    '<span>📞 <a href="tel:+50947385663">(509) 4738-5663</a></span>'
    '<span>✉️ <a href="mailto:deslandes78@gmail.com">deslandes78@gmail.com</a></span>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown("---")

# ============================================================
# BOOK AREA — current page
# ============================================================
current_page = PAGES[st.session_state.page_index]
page_num = st.session_state.page_index + 1

st.markdown(
    f'<div style="text-align:center;color:#8fa9d1;font-family:\'Courier New\',monospace;'
    f'font-weight:900;letter-spacing:2px;margin-bottom:8px;">'
    f'PAGE {page_num} / 100</div>',
    unsafe_allow_html=True,
)

# Book card
st.markdown(
    f'<div style="background:linear-gradient(180deg,#f5e6c8,#e2c98f);'
    f'border:3px solid #8a5a20;border-radius:18px;padding:26px 30px;'
    f'box-shadow:inset 0 0 80px rgba(120,70,20,.25), 0 20px 60px rgba(0,0,0,.7);">'
    f'<div class="page-title">{current_page["title"]}</div>'
    f'<div class="page-text">{current_page["text"]}</div>'
    f'</div>',
    unsafe_allow_html=True,
)

st.markdown("")

# ============================================================
# NAVIGATION BUTTONS
# ============================================================
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    if st.button("◀ Previous", use_container_width=True, disabled=(st.session_state.page_index == 0)):
        st.session_state.page_index -= 1
        st.rerun()

with col2:
    if st.button("Next ▶", use_container_width=True, disabled=(st.session_state.page_index >= 99)):
        st.session_state.page_index += 1
        st.rerun()

with col3:
    if st.button("↺ Restart", use_container_width=True):
        st.session_state.page_index = 0
        st.rerun()

with col4:
    st.metric("Page", f"{page_num}/100")

# ============================================================
# AI CHILD VOICE — text-to-speech
# ============================================================
st.markdown("---")
st.markdown(
    '<div style="text-align:center;font-size:.85rem;font-weight:900;'
    'letter-spacing:2px;color:#8fa9d1;margin-bottom:8px;">'
    '🔊 AI CHILD VOICE — READ THIS PAGE</div>',
    unsafe_allow_html=True,
)

if st.button("▶ Read This Page Aloud", use_container_width=True, type="primary"):
    with st.spinner("The voice is getting ready…"):
        try:
            tts = gTTS(
                text=f"{current_page['title']}. {current_page['text']}",
                lang="en",
                slow=False,
                tld="com",  # US female-sounding voice
            )
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            st.audio(audio_buffer, format="audio/mp3", autoplay=True)
        except Exception as e:
            st.error(f"Could not generate the voice: {e}")

# ============================================================
# PROGRESS BAR
# ============================================================
st.progress(page_num / 100)

# ============================================================
# QUICK JUMP — sidebar
# ============================================================
with st.sidebar:
    st.markdown("### 📖 Jump to a Page")
    jump = st.number_input("Page number (1–100)", min_value=1, max_value=100, value=page_num)
    if st.button("Go", use_container_width=True):
        st.session_state.page_index = int(jump) - 1
        st.rerun()

    st.markdown("---")
    st.markdown("### 👑 Britney's Kids")
    st.caption("Book 1 · 100 pages · Read aloud")
    st.caption("Built by Gesner Deslandes")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    '<div style="text-align:center;color:#8fa9d1;font-size:.75rem;'
    'letter-spacing:1.5px;font-weight:800;">'
    'BE LIKE BRIT · BRITNEY\'S KIDS IN WONDERLAND BOOK 1<br>'
    'Built by Gesner Deslandes · Technology Coordinator<br>'
    '(509) 4738-5663 · deslandes78@gmail.com'
    '</div>',
    unsafe_allow_html=True,
)
