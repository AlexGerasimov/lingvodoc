package ru.ispras.lingvodoc.frontend.app.services

import scala.scalajs.js
import com.greencatsoft.angularjs.injectable
import com.greencatsoft.angularjs.core.Promise

@js.native
@injectable("$modal")
trait ModalService extends js.Object {
  def open[T](options: ModalOptions): ModalInstance[T] = js.native
}

@js.native
trait ModalOptions extends js.Object {
  var template: String = js.native
  var templateUrl: String = js.native
  var controller: String = js.native
  var scope: Any = js.native
  var size: String = js.native
  var windowClass: String = js.native
  var backdrop: Boolean = js.native
  var keyboard: Boolean = js.native
  var resolve: js.Dictionary[js.Any] = js.native
}

object ModalOptions {
  def apply() = {
    val options = new js.Object().asInstanceOf[ModalOptions]
    options.size = "lg"
    options.resolve = js.Dictionary.empty
    options
  }
}

@js.native
@injectable("$modalInstance")
trait ModalInstance[T] extends js.Object {
  def close(result: T): Unit = js.native
  def close(): Unit = js.native
  def dismiss(reason: js.Any): Unit = js.native
  def result: Promise[T] = js.native
  def opened: Promise[Boolean] = js.native
}

