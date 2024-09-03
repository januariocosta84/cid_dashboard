document.addEventListener('DOMContentLoaded', function () {
    var titleInput = document.getElementById('id_title');
    var slugInput = document.getElementById('id_slug');

    if (titleInput && slugInput) {
        titleInput.addEventListener('keyup', function () {
            var title = titleInput.value;
            var slug = slugify(title);
            slugInput.value = slug;
        });
    }
});

function slugify(text) {
    return text.toString().toLowerCase().trim()
        .replace(/\s+/g, '-')           // Replace spaces with -
        .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
        .replace(/\-\-+/g, '-')         // Replace multiple - with single -
        .replace(/^-+/, '')             // Trim - from start of text
        .replace(/-+$/, '');            // Trim - from end of text
}
