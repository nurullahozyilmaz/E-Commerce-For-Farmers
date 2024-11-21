// market.js

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.querySelector('.btn-search');
    const contentDiv = document.querySelector('.content');

    searchButton.addEventListener('click', function () {
        const query = searchInput.value.trim();
        if (query !== '') {
            searchProducts(query);
        }
    });

    searchInput.addEventListener('keyup', function (event) {
        if (event.keyCode === 13) {
            const query = searchInput.value.trim();
            if (query !== '') {
                searchProducts(query);
            }
        }
    });

    function searchProducts(query) {
        fetch(`/search/?q=${query}`)
            .then(response => response.text())
            .then(data => {
                contentDiv.innerHTML = data;
            })
            .catch(error => console.error('Error:', error));
    }
});
