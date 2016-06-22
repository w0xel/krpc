import unittest
import krpctest

class TestPartsPart(krpctest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.new_save()
        if cls.connect().space_center.active_vessel.name != 'Parts':
            cls.launch_vessel_from_vab('Parts')
            cls.remove_other_vessels()
        cls.vessel = cls.connect().space_center.active_vessel
        cls.parts = cls.vessel.parts
        cls.far_available = cls.connect().space_center.far_available

    def test_root_part(self):
        part = self.parts.root
        self.assertEqual('Mark1-2Pod', part.name)
        self.assertEqual('Mk1-2 Command Pod', part.title)
        self.assertEqual(3800, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertIsNone(part.parent)
        self.assertItemsEqual(
            ['AE-FF1 Airstream Protective Shell (1.25m)'] + \
            ['LT-1 Landing Struts']*3 + \
            ['LY-10 Small Landing Gear', 'TR-XL Stack Separator'],
            [x.title for x in part.children])
        self.assertTrue(part.axially_attached)
        self.assertFalse(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(-1, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(4120, part.mass, places=4)
        self.assertAlmostEqual(4000, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(45, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = [
            'FlagDecal',
            'ModuleCommand',
            'ModuleConductionMultiplier',
            'ModuleReactionWheel',
            'ModuleScienceContainer',
            'ModuleScienceExperiment',
            'ModuleTripLogger',
            'TransferDialogSpawner'
        ]
        if self.far_available:
            modules.extend(['FARBasicDragModel', 'FARControlSys'])
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNone(part.cargo_bay)
        self.assertIsNone(part.control_surface)
        self.assertIsNone(part.decoupler)
        self.assertIsNone(part.docking_port)
        self.assertIsNone(part.engine)
        self.assertIsNone(part.fairing)
        self.assertIsNone(part.intake)
        self.assertIsNone(part.landing_gear)
        self.assertIsNone(part.landing_leg)
        self.assertIsNone(part.launch_clamp)
        self.assertIsNone(part.light)
        self.assertIsNone(part.parachute)
        self.assertIsNone(part.radiator)
        self.assertIsNone(part.rcs)
        self.assertIsNone(part.resource_converter)
        self.assertIsNone(part.resource_harvester)
        self.assertIsNotNone(part.reaction_wheel)
        self.assertIsNone(part.sensor)
        self.assertIsNone(part.solar_panel)

    def test_thermal(self):
        part = self.parts.root
        self.assertAlmostEqual(300, part.temperature, delta=50)
        self.assertAlmostEqual(300, part.skin_temperature, delta=50)
        self.assertEqual(1400, part.max_temperature)
        self.assertEqual(2400, part.max_skin_temperature)
        self.assertAlmostEqual(3.55, part.thermal_mass, places=2)
        self.assertAlmostEqual(0.0133, part.thermal_skin_mass, places=4)
        self.assertAlmostEqual(0.36, part.thermal_resource_mass, places=2)
        self.assertAlmostEqual(0, part.thermal_conduction_flux, places=2)
        self.assertAlmostEqual(0, part.thermal_convection_flux, places=2)
        self.assertAlmostEqual(0, part.thermal_radiation_flux, places=2)
        self.assertAlmostEqual(0, part.thermal_internal_flux, places=2)
        self.assertAlmostEqual(0, part.thermal_skin_to_internal_flux, places=2)

    def test_cargo_bay(self):
        part = self.parts.with_title('Service Bay (2.5m)')[0]
        self.assertEqual('ServiceBay.250', part.name)
        self.assertEqual('Service Bay (2.5m)', part.title)
        self.assertEqual(500, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Rockomax X200-8 Fuel Tank', part.parent.title)
        self.assertItemsEqual(['RE-L10 "Poodle" Liquid Fuel Engine'],
                              [p.title for p in part.children])
        self.assertTrue(part.axially_attached)
        self.assertFalse(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(1, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(300, part.mass, places=4)
        self.assertAlmostEqual(300, part.dry_mass, places=4)
        self.assertEqual(14, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = [
            'ModuleAnimateGeneric',
            'ModuleCargoBay',
            'ModuleConductionMultiplier',
            'ModuleSeeThroughObject'
        ]
        if self.far_available:
            modules.append('FARBasicDragModel')
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.cargo_bay)

    def test_control_surface(self):
        part = self.parts.with_title('Delta-Deluxe Winglet')[0]
        self.assertEqual('winglet3', part.name)
        self.assertEqual('Delta-Deluxe Winglet', part.title)
        self.assertEqual(600, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Rockomax X200-32 Fuel Tank', part.parent.title)
        self.assertEqual([], part.children)
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(3, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(78, part.mass, places=4)
        self.assertAlmostEqual(78, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(12, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['ModuleControlSurface']
        if self.far_available:
            modules.append('FARBasicDragModel')
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.control_surface)

    def test_decoupler(self):
        part = self.parts.with_title('TT-70 Radial Decoupler')[0]
        self.assertEqual('radialDecoupler2', part.name)
        self.assertEqual('TT-70 Radial Decoupler', part.title)
        self.assertEqual(700, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Rockomax Jumbo-64 Fuel Tank', part.parent.title)
        self.assertItemsEqual(['S1 SRB-KD25k "Kickback" Solid Fuel Booster'],
                              [p.title for p in part.children])
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(5, part.stage)
        self.assertEqual(5, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(50, part.mass, places=4)
        self.assertAlmostEqual(50, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(8, part.impact_tolerance)
        self.assertFalse(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['ModuleAnchoredDecoupler', 'ModuleTestSubject', 'ModuleToggleCrossfeed']
        if self.far_available:
            modules.append('FARBasicDragModel')
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.decoupler)

    def test_docking_port(self):
        part = self.parts.with_title('Clamp-O-Tron Docking Port')[0]
        self.assertEqual('dockingPort2', part.name)
        self.assertEqual('Clamp-O-Tron Docking Port', part.title)
        self.assertEqual(280, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Rockomax X200-32 Fuel Tank', part.parent.title)
        self.assertEqual([], part.children)
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        #TODO: why is this not -1? Docking ports aren't activated in stages?
        self.assertEqual(4, part.stage)
        self.assertEqual(3, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(50, part.mass, places=4)
        self.assertAlmostEqual(50, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(10, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['ModuleDockingNode']
        if self.far_available:
            modules.append('FARBasicDragModel')
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.docking_port)

    def test_engine(self):
        part = self.parts.with_title('S1 SRB-KD25k "Kickback" Solid Fuel Booster')[0]
        self.assertEqual('MassiveBooster', part.name)
        self.assertEqual('S1 SRB-KD25k "Kickback" Solid Fuel Booster', part.title)
        self.assertEqual(2700, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('TT-70 Radial Decoupler', part.parent.title)
        self.assertItemsEqual(['Aerodynamic Nose Cone'], [p.title for p in part.children])
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(6, part.stage)
        self.assertEqual(5, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(23250, part.mass, places=4)
        self.assertAlmostEqual(4500, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(7, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['FXModuleAnimateThrottle', 'ModuleEnginesFX', 'ModuleSurfaceFX', 'ModuleTestSubject']
        if self.far_available:
            modules.append('FARBasicDragModel')
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.engine)

    def test_fairing(self):
        part = self.parts.with_title('AE-FF1 Airstream Protective Shell (1.25m)')[0]
        self.assertEqual('fairingSize1', part.name)
        self.assertEqual('AE-FF1 Airstream Protective Shell (1.25m)', part.title)
        self.assertEqual(900, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Mk1-2 Command Pod', part.parent.title)
        self.assertEqual([], part.children)
        self.assertTrue(part.axially_attached)
        self.assertFalse(part.radially_attached)
        self.assertEqual(0, part.stage)
        self.assertEqual(-1, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(121.74388, part.mass, places=4)
        self.assertAlmostEqual(121.74388, part.dry_mass, places=4)
        self.assertEqual(9, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['ModuleCargoBay', 'ModuleProceduralFairing', 'ModuleTestSubject']
        if self.far_available:
            modules.append('FARBasicDragModel')
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.fairing)

    def test_intake(self):
        part = self.parts.with_title('XM-G50 Radial Air Intake')[0]
        self.assertEqual('airScoop', part.name)
        self.assertEqual('XM-G50 Radial Air Intake', part.title)
        self.assertEqual(250, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Rockomax X200-8 Fuel Tank', part.parent.title)
        self.assertEqual([], part.children)
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(1, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(30, part.mass, places=4)
        #TODO: why is the dry mass != total mass, part doens't have any resources!?
        self.assertAlmostEqual(20, part.dry_mass, places=4)
        self.assertEqual(10, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['ModuleResourceIntake']
        if self.far_available:
            modules.append('FARBasicDragModel')
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.intake)

    def test_landing_gear(self):
        part = self.parts.with_title('LY-10 Small Landing Gear')[0]
        self.assertEqual('SmallGearBay', part.name)
        self.assertEqual('LY-10 Small Landing Gear', part.title)
        self.assertEqual(600, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Mk1-2 Command Pod', part.parent.title)
        self.assertEqual([], [p.title for p in part.children])
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(-1, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(45, part.mass, places=4)
        self.assertAlmostEqual(45, part.dry_mass, places=4)
        self.assertEqual(50, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = [
            'FXModuleConstrainPosition',
            'FXModuleLookAtConstraint',
            'ModuleLight',
            'ModuleStatusLight',
            'ModuleTestSubject',
            'ModuleWheelBase',
            'ModuleWheelBrakes',
            'ModuleWheelDamage',
            'ModuleWheelDeployment',
            'ModuleWheelSteering',
            'ModuleWheelSuspension'
        ]
        if self.far_available:
            modules.append('FARBasicDragModel')
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.landing_gear)

    def test_landing_leg(self):
        part = self.parts.with_title('LT-1 Landing Struts')[0]
        self.assertEqual('landingLeg1', part.name)
        self.assertEqual('LT-1 Landing Struts', part.title)
        self.assertEqual(440, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Mk1-2 Command Pod', part.parent.title)
        self.assertEqual([], part.children)
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(-1, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(50, part.mass, places=4)
        self.assertAlmostEqual(50, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(12, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = [
            'ModuleWheelBase',
            'ModuleWheelBogey',
            'ModuleWheelDamage',
            'ModuleWheelDeployment',
            'ModuleWheelLock',
            'ModuleWheelSuspension'
        ]
        if self.far_available:
            modules.append('FARBasicDragModel')
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.landing_leg)

    def test_launch_clamp(self):
        part = self.parts.with_title('TT18-A Launch Stability Enhancer')[0]
        self.assertEqual('launchClamp1', part.name)
        self.assertEqual('TT18-A Launch Stability Enhancer', part.title)
        self.assertEqual(200, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Rockomax Jumbo-64 Fuel Tank', part.parent.title)
        self.assertEqual([], part.children)
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(6, part.stage)
        self.assertEqual(6, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(100, part.mass, places=4)
        self.assertAlmostEqual(100, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(100, part.impact_tolerance)
        self.assertFalse(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['LaunchClamp', 'ModuleGenerator', 'ModuleTestSubject']
        actual_modules = [x.name for x in part.modules]
        if 'ModuleRTAntennaPassive' in actual_modules:
            actual_modules.remove('ModuleRTAntennaPassive')
        self.assertItemsEqual(modules, actual_modules)
        self.assertIsNotNone(part.launch_clamp)

    def test_light(self):
        part = self.parts.with_title('Illuminator Mk1')[0]
        self.assertEqual('spotLight1', part.name)
        self.assertEqual('Illuminator Mk1', part.title)
        self.assertEqual(100, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Aerodynamic Nose Cone', part.parent.title)
        self.assertEqual([], part.children)
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(5, part.decouple_stage)
        self.assertTrue(part.massless)
        self.assertAlmostEqual(0, part.mass, places=4)
        self.assertAlmostEqual(0, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(8, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['ModuleLight']
        if self.far_available:
            modules.append('FARBasicDragModel')
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.light)

    def test_parachute(self):
        part = self.parts.with_title('Mk2-R Radial-Mount Parachute')[0]
        self.assertEqual('parachuteRadial', part.name)
        self.assertEqual('Mk2-R Radial-Mount Parachute', part.title)
        self.assertEqual(400, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Rockomax X200-8 Fuel Tank', part.parent.title)
        self.assertEqual([], part.children)
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(2, part.stage)
        self.assertEqual(1, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(100, part.mass, places=4)
        self.assertAlmostEqual(100, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(12, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        self.assertItemsEqual(
            ['ModuleDragModifier', 'ModuleDragModifier',
             'ModuleParachute', 'ModuleTestSubject'],
            [x.name for x in part.modules])
        self.assertIsNotNone(part.parachute)

    def test_radiator(self):
        part = self.parts.with_title('Thermal Control System (small)')[0]
        self.assertEqual('foldingRadSmall', part.name)
        self.assertEqual('Thermal Control System (small)', part.title)
        self.assertEqual(450, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Advanced Reaction Wheel Module, Large', part.parent.title)
        self.assertEqual([], part.children)
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(3, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(50, part.mass, places=4)
        self.assertAlmostEqual(50, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(12, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['ModuleActiveRadiator', 'ModuleDeployableRadiator']
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.radiator)

    def test_rcs(self):
        part = self.parts.with_title('RV-105 RCS Thruster Block')[0]
        self.assertEqual('RCSBlock', part.name)
        self.assertEqual('RV-105 RCS Thruster Block', part.title)
        self.assertEqual(620, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Rockomax X200-8 Fuel Tank', part.parent.title)
        self.assertEqual([], part.children)
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(1, part.decouple_stage)
        self.assertTrue(part.massless)
        self.assertAlmostEqual(0, part.mass, places=4)
        self.assertAlmostEqual(0, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(15, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['ModuleRCS']
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.rcs)

    def test_reaction_wheel(self):
        part = self.parts.with_title('Advanced Reaction Wheel Module, Large')[0]
        self.assertEqual('asasmodule1-2', part.name)
        self.assertEqual('Advanced Reaction Wheel Module, Large', part.title)
        self.assertEqual(2100, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('FL-R1 RCS Fuel Tank', part.parent.title)
        self.assertItemsEqual(['Thermal Control System (small)', 'Convert-O-Tron 250'],
                              [p.title for p in part.children])
        self.assertTrue(part.axially_attached)
        self.assertFalse(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(3, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(200, part.mass, places=4)
        self.assertAlmostEqual(200, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(9, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['ModuleReactionWheel']
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.reaction_wheel)

    def test_resource_converter(self):
        part = self.parts.with_title('Convert-O-Tron 250')[0]
        self.assertEqual('ISRU', part.name)
        self.assertEqual('Convert-O-Tron 250', part.title)
        self.assertEqual(8000, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Advanced Reaction Wheel Module, Large', part.parent.title)
        self.assertItemsEqual(['Rockomax X200-32 Fuel Tank'], [p.title for p in part.children])
        self.assertTrue(part.axially_attached)
        self.assertFalse(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(3, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(4250, part.mass, places=4)
        self.assertAlmostEqual(4250, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(7, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['ModuleAnimationGroup',
                   'ModuleCoreHeat',
                   'ModuleOverheatDisplay'] + \
                   ['ModuleResourceConverter']*4
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.resource_converter)

    def test_resource_harvester(self):
        part = self.parts.with_title('\'Drill-O-Matic Junior\' Mining Excavator')[0]
        self.assertEqual('MiniDrill', part.name)
        self.assertEqual('\'Drill-O-Matic Junior\' Mining Excavator', part.title)
        self.assertEqual(1000, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Rockomax X200-32 Fuel Tank', part.parent.title)
        self.assertEqual([], part.children)
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(3, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(250, part.mass, places=4)
        self.assertAlmostEqual(250, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(7, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = [
            'ModuleAnimationGroup',
            'ModuleAsteroidDrill',
            'ModuleCoreHeat',
            'ModuleOverheatDisplay',
            'ModuleResourceHarvester'
        ]
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.resource_harvester)

    def test_sensor(self):
        part = self.parts.with_title('PresMat Barometer')[0]
        self.assertEqual('sensorBarometer', part.name)
        self.assertEqual('PresMat Barometer', part.title)
        self.assertEqual(3300, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('Rockomax X200-8 Fuel Tank', part.parent.title)
        self.assertEqual([], part.children)
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(1, part.decouple_stage)
        self.assertTrue(part.massless)
        self.assertAlmostEqual(0, part.mass, places=4)
        self.assertAlmostEqual(0, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(8, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['ModuleEnviroSensor', 'ModuleScienceExperiment']
        if self.far_available:
            modules.append('FARBasicDragModel')
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.sensor)

    def test_solar_panel(self):
        part = self.parts.with_title('Gigantor XL Solar Array')[0]
        self.assertEqual('largeSolarPanel', part.name)
        self.assertEqual('Gigantor XL Solar Array', part.title)
        self.assertEqual(3000, part.cost)
        self.assertEqual(self.vessel, part.vessel)
        self.assertEqual('FL-R1 RCS Fuel Tank', part.parent.title)
        self.assertEqual([], part.children)
        self.assertFalse(part.axially_attached)
        self.assertTrue(part.radially_attached)
        self.assertEqual(-1, part.stage)
        self.assertEqual(3, part.decouple_stage)
        self.assertFalse(part.massless)
        self.assertAlmostEqual(300, part.mass, places=4)
        self.assertAlmostEqual(300, part.dry_mass, places=4)
        self.assertFalse(part.shielded)
        self.assertAlmostEqual(0, part.dynamic_pressure, places=4)
        self.assertEqual(8, part.impact_tolerance)
        self.assertTrue(part.crossfeed)
        self.assertFalse(part.is_fuel_line)
        self.assertEqual([], part.fuel_lines_from)
        self.assertEqual([], part.fuel_lines_to)
        modules = ['ModuleDeployableSolarPanel']
        if self.far_available:
            modules.append('FARBasicDragModel')
        self.assertItemsEqual(modules, [x.name for x in part.modules])
        self.assertIsNotNone(part.solar_panel)

if __name__ == '__main__':
    unittest.main()