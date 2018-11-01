"""
Config for displaying MLN's models in the django admin.
Most of the code here is for displaying various settings models inline with the model admin interface they correspond to, for example showing blueprint requirements for a blueprint item.
"""
from django.apps import apps
from django.contrib import admin

from ..models.dynamic import Attachment, Friendship, Message, Profile, InventoryStack
from ..models.module import Module, ModuleSaveConcertArcade, ModuleSaveSoundtrack, module_settings_classes
from ..models.module_settings_arcade import DeliveryArcadeTile
from ..models.static import Answer, ArcadePrize, BlueprintInfo, BlueprintRequirement, ItemInfo, ItemType, MessageBody, ModuleEditorType, ModuleExecutionCost, ModuleInfo, ModuleSetupCost, ModuleYieldInfo, StartingStack, Question
from .make_inline import custom, inlines, make_inline

# Normal but customized admin interfaces

class MessageBodyAdmin(admin.ModelAdmin):
	list_display = "subject", "text"
	search_fields = list_display
	filter_vertical = "easy_replies",

custom[MessageBody] = MessageBodyAdmin

class DeliveryArcadeTileAdmin(admin.ModelAdmin):
	list_display = "module", "tile_id", "x", "y"

custom[DeliveryArcadeTile] = DeliveryArcadeTileAdmin

class StackAdmin(admin.ModelAdmin):
	list_display = "qty", "item"
	list_display_links = "item",
	search_fields = "item__name",
	list_filter = "item__type",

custom[StartingStack] = StackAdmin

class InventoryStackAdmin(StackAdmin):
	list_display = ("owner",) + StackAdmin.list_display
	search_fields = ("owner__username",) + StackAdmin.search_fields
	list_filter = ("owner",) + StackAdmin.list_filter

custom[InventoryStack] = InventoryStackAdmin

# Inline display functions

def get_item_info_inlines(obj):
	if obj.type == ItemType.BLUEPRINT:
		yield BlueprintInfo
		yield BlueprintRequirement
	elif obj.type == ItemType.MODULE:
		yield ModuleInfo
		yield ModuleYieldInfo
		if obj.module_info.is_executable:
			yield ModuleExecutionCost
		if obj.module_info.is_setupable:
			yield ModuleSetupCost
		if obj.module_info.editor_type in (ModuleEditorType.CONCERT_I_ARCADE, ModuleEditorType.CONCERT_II_ARCADE, ModuleEditorType.DELIVERY_ARCADE, ModuleEditorType.DESTRUCTOID_ARCADE, ModuleEditorType.DR_INFERNO_ROBOT_SIM, ModuleEditorType.HOP_ARCADE):
			yield	ArcadePrize

def get_settings_inlines(obj):
	inlines = obj.get_settings_classes()
	if inlines == (ModuleSaveConcertArcade,):
		yield ModuleSaveConcertArcade
		yield ModuleSaveSoundtrack
	else:
		yield from inlines

# Misc inlines

make_inline(Question, Answer)

make_inline(Profile, (Friendship, {"fk_name": "to_profile"}), (Friendship, {"fk_name": "from_profile"}))

message_admin = make_inline(Message, Attachment)
message_admin.list_display = "sender", "recipient", "body", "is_read"
message_admin.list_display_links = "body",
message_admin.list_filter = "recipient", "sender"

# Item infos

item_info_admin = make_inline(ItemInfo, ModuleInfo, (ArcadePrize, {"fk_name": "module_item"}), (ModuleExecutionCost, {"fk_name": "module_item"}), (ModuleSetupCost, {"fk_name": "module_item"}), (ModuleYieldInfo, {"fk_name": "item"}), (BlueprintInfo, {"fk_name": "item"}), (BlueprintRequirement, {"fk_name": "blueprint_item"}), get_inlines=get_item_info_inlines)
item_info_admin.list_display = "name", "type"
item_info_admin.search_fields = "name",
item_info_admin.list_filter = "type",

# Modules & module settings

settings = set()
for classes in module_settings_classes.values():
	for cls in classes:
		settings.add(cls)

module_admin = make_inline(Module, *settings, get_inlines=get_settings_inlines)
module_admin.list_display = "owner", "item", "pos_x", "pos_y", "total_clicks"
module_admin.list_display_links = "item",
module_admin.list_filter = "owner",

# Register admin interfaces

for model in apps.get_app_config("mln").get_models():
	if model in custom:
		admin.site.register(model, custom[model])
	elif model not in inlines:
		admin.site.register(model)