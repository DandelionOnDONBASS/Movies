function ajaxSend(url, params) {
    // Отправляем запрос
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json()) // Преобразование JSON-ответа
        .then(json => {
            updateMovies(json.movies); // Обновление шаблона с помощью функции updateMovies
        })
        .catch(error => console.error(error))
}

// Filter movies
// const forms = document.querySelector('form[name=filter]');
//
// forms.addEventListener('submit', function (e) {
//    console.log('ddddddddd')
//     // Получаем данные из формы
//     e.preventDefault();
//     let url = this.action;
//     let params = new URLSearchParams(new FormData(this)).toString();
//     ajaxSend(url, params);
// });

function updateMovies(movies) {
  const containerElement = document.querySelector('.left-ads-display .row');
  containerElement.innerHTML = ''; // Clear existing content

  for (const movie of movies) {
    const movieElement = document.createElement('div');
    movieElement.classList.add('col-md-4', 'product-men');

    // Add movie HTML using string interpolation or template literals
    movieElement.innerHTML = `
      <div class="product-shoe-info editContent text-center mt-lg-4" >
        <div class="men-thumb-item">
          <img src="/media/${ movie.poster }" class="img-fluid" alt="" >
        </div>
        <div class="item-info-product">
          <h4 class="">
            <a href="/${movie.url}" class="editContent" >${movie.title}</a>
          </h4>
          <div class="product_price">
            <div class="grid-price">
              <span class="money editContent" >${movie.tagline}</span>
            </div>
          </div>
          <ul class="stars">
            <li><a href="#"><span class="fa fa-star" aria-hidden="true" ></span></a></li>
            <li><a href="#"><span class="fa fa-star" aria-hidden="true" ></span></a></li>
            <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true" ></span></a></li>
            <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true" ></span></a></li>
            <li><a href="#"><span class="fa fa-star-o" aria-hidden="true" ></span></a></li>
          </ul>
        </div>
      </div>
    `;

    containerElement.appendChild(movieElement);
  }
}


// Add star rating
// Add star rating
const rating = document.querySelector('form[name=rating]');

rating.addEventListener("change", function (e) {
    // Получаем данные из формы
    let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
        .then(response => alert("Рейтинг установлен"))
        .catch(error => alert("Ошибка"))
});