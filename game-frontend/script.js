document.getElementById("loadBtn").addEventListener("click", () => {
    const user_id = document.getElementById("userInput").value;
    const container = document.getElementById("games");
    container.innerHTML = "";

    if (!user_id) {
        container.innerHTML = "<p>Введи Telegram id</p>";
        return;
    }

    fetch(`https://game-shelf-bot.onrender.com/games/user/${user_id}`)
        .then(response => response.json())
        .then(games => {
            if (games.length === 0) {
                container.innerHTML = "<p>У тебя пока нет игр</p>";
                return;
            }

            games.forEach(game => {
                const card = document.createElement("div");
                card.className = "card";
                card.innerHTML = `
                    <h3>${game.title}</h3>
                    <p>${game.status}</p>
                    <span>${game.date}</span>
                `;
                container.appendChild(card);
            });
        })
        .catch(error => {
            container.innerHTML = "<p>Ошибка загрузки</p>";
            console.error(error);
        });
});