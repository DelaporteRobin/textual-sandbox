from __future__ import annotations

from typing import ClassVar, Iterable, Optional

from typing_extensions import TypeGuard

from textual._loop import loop_from_index
from textual.await_complete import AwaitComplete
from textual.await_remove import AwaitRemove
from textual.binding import Binding, BindingType
from textual.containers import VerticalScroll
from textual.events import Mount
from textual.message import Message
from textual.reactive import reactive
from textual.widget import AwaitMount
from textual.widgets._list_item import ListItem

from textual.app import App, ComposeResult
from textual.widgets import ListView, Button, Label
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.screen import Screen 
from textual import events
from textual import work
from textual import on
from textual.await_complete import AwaitComplete 
from textual.errors import TextualError


from textual import events, on
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget


class MultiListItem(ListItem):
	"""A widget that is an item within a `ListView`.

	A `ListItem` is designed for use within a
	[ListView][textual.widgets._list_view.ListView], please see `ListView`'s
	documentation for more details on use.
	""" 

	#highlighted = reactive(False)
	highlight_list = []
	"""Is this item highlighted?"""

	def watch_highlighted(self, value: bool) -> None:
		#self.notify(str(self in self.highlight_list))
		if self in self.highlight_list:
			self.set_class(True, "-highlight")
		else:
			self.set_class(value, "-highlight")
		
		"""
		conditions to highlight an object
		1 - current object selected
		2 - object in the list
		"""

	def highlight_item(self, item) -> None:

		if item not in self.highlight_list:
			self.highlight_list.append(item)
			self.highlighted=True
		else:
			self.highlight_list.remove(item)
			self.highlighted = False

		for element in self.highlight_list:
			element.highlighted = True

	@on(events.Enter)
	@on(events.Leave)
	def on_enter_or_leave(self, event: events.Enter | events.Leave) -> None:
		event.stop()
		self.set_class(self.is_mouse_over, "-hovered")






class ListViewMulti(ListView):
	index_list = reactive[list]([], init=False)

	@property
	def highlighted_child(self) -> ListItem | None:
		"""The currently highlighted ListItem, or None if nothing is highlighted."""
		if self.index is not None and 0 <= self.index < len(self._nodes):
			list_item = self._nodes[self.index]

			if self.index not in self.index_list:
				self.index_list.append(self.index)
			else:
				self.index_list.remove(self.index)


			assert isinstance(list_item, ListItem)
			return list_item
		else:
			return None







class TestApp(App):


	def compose(self) -> ComposeResult:

		self.test_listview = ListViewMulti(id = "test_listview")
		yield self.test_listview
		yield Button("GET", id="button_get")


	def on_mount(self) -> None:
		for i in range(10):
			label = Label("hello world : %s"%i)
			self.test_listview.append(MultiListItem(label))

		


	def on_key(self, event:events.Key) -> None:
		#self.notify(str(self.focused))
		#self.notify(str(self.focused.id == "test_listview"))
		if event.key == "enter":
			if self.focused.id == "test_listview":
				#self.test_listview.highlight_listitem()
				#get children with the index
				children_item = self.test_listview.children[self.test_listview.index]
				children_item.highlight_item(children_item)


	def on_button_pressed(self, event:Button.Pressed) -> None:
		if event.control.id == "button_get":
			self.notify("hello world", timeout=1)
			self.notify(str(self.test_listview.index))
			self.notify(str(self.test_listview.index_list))


if __name__ == "__main__":
	app = TestApp()
	app.run()