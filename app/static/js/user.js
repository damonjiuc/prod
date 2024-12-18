var modal-callback = document.getElementById('modal-callback')
var modal-btn-callback = document.getElementById('modal-btn-callback')
var modal-order = document.getElementById('modal-order')
var modal-btn-order = document.getElementById('modal-btn-order')
var modal-feedback = document.getElementById('modal-feedback')
var modal-btn-feedback = document.getElementById('modal-btn-feedback')
var modal-reminder = document.getElementById('modal-reminder')
var modal-btn-reminder = document.getElementById('modal-btn-reminder')
var modal-news = document.getElementById('modal-news')
var modal-btn-news = document.getElementById('modal-btn-news')
var modal-goods = document.getElementById('modal-goods')
var modal-btn-goods = document.getElementById('modal-btn-goods')

modal-callback.addEventListener('shown.bs.modal', function () {
  modal-btn-callback.focus();
})
modal-order.addEventListener('shown.bs.modal', function () {
  modal-btn-order.focus();
})
modal-feedback.addEventListener('shown.bs.modal', function () {
  modal-btn-feedback.focus();
})
modal-reminder.addEventListener('shown.bs.modal', function () {
  modal-btn-reminder.focus();
})
modal-news.addEventListener('shown.bs.modal', function () {
  modal-btn-news.focus();
})
modal-goods.addEventListener('shown.bs.modal', function () {
  modal-btn-goods.focus();
})

function copyRefLink(link) {
    navigator.clipboard.writeText(link);
}