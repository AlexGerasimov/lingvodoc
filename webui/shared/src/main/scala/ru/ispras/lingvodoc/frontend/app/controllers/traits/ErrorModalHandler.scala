package ru.ispras.lingvodoc.frontend.app.controllers.traits

import com.greencatsoft.angularjs.extensions.{ModalOptions, ModalService}

import scala.scalajs.js


trait ErrorModalHandler {

  def modal: ModalService

  def showError(e: Throwable) = {
    val options = ModalOptions()
    options.templateUrl = "/static/templates/modal/exceptionHandler.html"
    options.controller = "ExceptionHandlerController"
    options.backdrop = false
    options.keyboard = false
    options.size = "lg"
    options.resolve = js.Dynamic.literal(
      params = () => {
        js.Dynamic.literal(exception = e.asInstanceOf[js.Any])
      }
    ).asInstanceOf[js.Dictionary[Any]]

    val instance = modal.open[Unit](options)
  }
}
