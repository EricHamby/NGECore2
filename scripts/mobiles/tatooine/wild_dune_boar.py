import sys
from services.spawn import MobileTemplate
from services.spawn import WeaponTemplate
from java.util import Vector

def addTemplate(core):
	mobileTemplate = MobileTemplate()
	
	mobileTemplate.setCreatureName('wild_dune_boar')
	mobileTemplate.setLevel(50)
	mobileTemplate.setMinLevel(49)
	mobileTemplate.setMaxLevel(51)
	mobileTemplate.setDifficulty(0)
	mobileTemplate.setAttackRange(5)
	mobileTemplate.setAttackSpeed(1.0)
	mobileTemplate.setWeaponType(6)
	mobileTemplate.setMinSpawnDistance(4)
	mobileTemplate.setMaxSpawnDistance(8)
	mobileTemplate.setDeathblow(True)
	mobileTemplate.setScale(1)
	mobileTemplate.setMeatType("Herbivore Meat")
	mobileTemplate.setMeatAmount(90)
	mobileTemplate.setHideType("Leathery Hide")
	mobileTemplate.setBoneAmount(80)	
	mobileTemplate.setBoneType("Animal Bone")
	mobileTemplate.setHideAmount(75)
	mobileTemplate.setSocialGroup("zucca boar")
	mobileTemplate.setAssistRange(12)
	mobileTemplate.setStalker(False)
	
	templates = Vector()
	templates.add('object/mobile/shared_zucca_boar.iff')
	mobileTemplate.setTemplates(templates)

	weaponTemplates = Vector()
	weapontemplate = WeaponTemplate('object/weapon/melee/unarmed/shared_unarmed_default.iff', 6, 1.0)
	weaponTemplates.add(weapontemplate)
	mobileTemplate.setWeaponTemplateVector(weaponTemplates)
	
	attacks = Vector()
	mobileTemplate.setDefaultAttack('creatureMeleeAttack')
	attacks.add('bm_charge_2')
	attacks.add('bm_dampen_pain_2')
	attacks.add('bm_slash_2')
	mobileTemplate.setAttacks(attacks)
	
	core.spawnService.addMobileTemplate('wild_dune_boar', mobileTemplate)
	return