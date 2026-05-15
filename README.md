# Baristapp
#### Video Demo:  https://youtu.be/QI13fNwBW7A
#### Description:
## What it does:

Baristapp is a web application that helps you register your coffee recipes and, if needed, improve or fix them to achieve a better coffee extraction.

---

## Inspiration:

This project was created for coffee enthusiasts. When you are new to the world of specialty coffee, creating your own recipes and preparing a good cup of coffee can be a little overwhelming; water temperature, coffee grams, ratios, etc. Without guidance, it can be frustrating not knowing which variable to change when the coffee we prepare does not taste good. With this app, you only need to tell the AI what you dislike about your coffee so that, with the provided data, it knows what to change to improve your coffee.

I chose something related to coffee because it is one of my hobbies and favorite activities. Searching for the perfect recipe and noticing the different notes of specialty coffee is amazing. The idea was born because I usually wrote my personal recipes in a paper notebook. If I did not like a recipe, it became tedious not knowing what to change. With this project I can have a database of my recipes and, if there is something I dislike, I can easily solve it with the help of AI.

---

## Problem to solve:

Normally, using my paper notebook was nice for writing recipes by hand, but improving them later was tedious. Without help, changing each variable and experimenting can become frustrating, and in the world of coffee brewing, a small change greatly affects the extraction result. I found Android apps that only serve to save recipes, but none that directly help improve them. With Baristapp I can save recipes, compare them, and improve them in a practical way.

---

## Technologies used:

I used HTML and Bootstrap to build a responsive and intuitive interface. Bootstrap allowed me to quickly design forms, cards, and navigation adaptable to mobile devices.

```html
<div class="mb-3">
    <label for="ratio" class="form-label d-block text-center">Ratio 1:</label>
    <input type="number" id="ratio" name="ratio" class="form-control form-control-lg" required>
</div>
```

I used JavaScript to add interactivity, especially using fetch to send recipe data to the AI without reloading the page.

```javascript
fetch("/mejorar_receta", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({nombre, g_cafe, temp, ratio, infusion, comentario})
})
.then(res => res.json())
.then(data => {
    card.innerHTML = `<div class="alert alert-info">${data.consejo}</div>`;
});
```

The backend was developed with Flask, which I used to handle routes, forms, and communication between the frontend, SQLite, and the AI API.

Recipes are stored in SQLite, allowing information such as coffee grams, ratio, temperature, infusion time, and comments to be saved.

For the artificial intelligence integration, I used Hugging Face Router with an LLM model compatible with the OpenAI API such as DeepSeek. The AI receives the recipe parameters together with user feedback, for example “my coffee tasted bitter”, and generates recommendations to improve the preparation by modifying some parameters according to the rules I placed in system.

```python
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key="YOUR_API_KEY"
)

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V4-Pro:novita",
    messages=[
        {
            "role": "system",
            "content": "Respond as an expert barista giving advice to non-professional coffee enthusiasts, taking into account the parameters of a French press recipe and recommending how to improve it by altering only one or two of the given parameters. Respond briefly, maximum 90 words."
        },
        {
            "role": "user",
            "content": receta_str
        }
    ],
)

consejo = completion.choices[0].message.content

return jsonify({"consejo": consejo})
```

---

## Project Architecture:

Baristapp follows a classic Flask app structure. It separates frontend, backend, and static files to keep everything organized.

In app.py are the Flask routes and the SQLite connection. Here the user inputs are received, sent to the database, and if requested by the user, the inputs and feedback are sent to the AI to improve the recipe through Hugging Face Router. The LLM model I use is DeepSeek v4.

Inside the templates folder are all the HTML pages of the app. I implemented a layout.html file to avoid repeating unnecessary code in every file, such as the navigation bar and site structure. Index, Metodos, Tips, and Recetas extend the template using Jinja.

Recetas.html is practically the most important page of the project, since all inputs are entered there, recipes are saved, saved recipes are displayed using dynamic cards, and the AI can improve them without reloading the page thanks to the JS integration.

The static folder contains the styles.css file that gives the project its visual style.

The database is called recetas.db and inside it are stored the recipe name, coffee grams, temperature, ratio, infusion time, and user comments.

I left database.py for future implementations. It is very likely that I will need to modify the database, and for me it is more practical to keep the template.

---

## Important Features:

Recipe storage is one of the central parts of the app. The user must obligatorily enter the recipe name, coffee grams, ratio, and infusion time. Comments are optional.

Saved recipes are displayed from newest to oldest. All entered parameters are shown, and the comments section only appears if comments exist. There is also a button connected to the backend to directly delete the recipe.

The second feature, and the one that gives the app a huge advantage, is the AI integration. Each recipe card has an “Improve recipe” button where the user can write what went wrong with the coffee or what they did not like.

Based on the instructions I gave the AI model, it must respond as an expert barista helping people who are not exactly experts on the subject. Its response is based on the recipe data sent through Flask, which receives them in JSON format and dynamically creates the prompt. The response is displayed below the recipe inside a blue box.

During the initial development, recipe information was obtained using positions inside the DOM. Later I thought it would be better to use data-attributes to associate the data with the corresponding card.

---

## Current limitations:

### The AI can be inconsistent:
Sometimes it ignores recipe comments or gives too much information. Other times it takes too long to respond.

### There is only one extraction method:
At the moment only French press recipes are implemented, which can limit its use for people who enjoy using more elaborate brewing methods.

### Saved recipes cannot be edited:
There is still no button that allows editing an existing recipe, the only option is to create it again.

---

## Future Improvements:

### New methods:
The first thing I want to do is implement recipes for Eye Dripper. I consider it a filtered brewing method less complicated than the V60 because of its flat bed, making it perfect for non-professionals. The implementation should not be too complex; I would need to add a dropdown menu at the top to choose the brewing method and then add inputs for pours and pauses between them.

### Edit button:
For a second revision, an edit button could be implemented to modify existing recipes without having to delete and rewrite them again.

### Dedicated server:
Running locally is a bit annoying and impractical. It could be connected to the NAS in my house so it can work without using Codespace.


