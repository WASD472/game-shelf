const urlParams = new URLSearchParams(window.location.search);//window.location.search — часть адреса после ?
const user_id_from_url = urlParams.get('user');

if (user_id_from_url) {
    document.getElementById("userInput").value = user_id_from_url;
    window.addEventListener('load', () => { // «когда страница полностью загрузится, автоматически нажать кнопку
        document.getElementById("loadBtn").click();
    });
}


document.getElementById("loadBtn").addEventListener("click", () => {
    const user_id = document.getElementById("userInput").value;
    const container = document.getElementById("games");
    container.innerHTML = "";

    if (!user_id) {
        container.innerHTML = "<p class='empty-msg'>Введи Telegram id</p>";
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
                let statusClass = "";
                if(game.status == "Пройдено") statusClass = "status-done";
                else if(game.status == "Играю") statusClass = "status-playing";
            
                const card = document.createElement("div");
                card.className = "card";
                card.innerHTML = `
                    <h3 class="card__title">${game.title}</h3>
                    <span class="card__status ${statusClass}">${game.status}</span>
                    <span class="card__date">${game.date}</span>
                `;
                container.appendChild(card);
             });

        })
        .catch(error => {
            container.innerHTML = "<p>Ошибка загрузки</p>";
            console.error(error);
        });
});