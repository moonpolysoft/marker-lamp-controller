/*
  Preliminary auxiliary marker-lamp controller enclosure.
  Units: millimeters.

  Export base and lid separately by changing `part`.
*/

part = "assembly"; // "base", "lid", or "assembly"

inside_length = 90;
inside_width = 74;
inside_height = 30;
wall = 3;
floor_thickness = 3;
lid_thickness = 3;
corner_radius = 5;
lid_clearance = 0.30;

lid_screw_clearance_diameter = 3.6;
lid_insert_hole_diameter = 4.2;
lid_insert_depth = 5.5;
screw_boss_diameter = 9;
screw_edge_offset = 11;

pcb_length = 80;
pcb_width = 45;
pcb_hole_spacing_x = 72;
pcb_hole_spacing_y = 37;
pcb_standoff_height = 5;
pcb_screw_diameter = 2.7;
pcb_shift_x = -4.5;

// Opening for the 4-position TBP01P1-508 mating plug.  The plug is
// 20.32 mm long and approximately 15 x 18 mm in cross-section.  A top-open
// notch avoids an unsupported bridge and permits insertion from outside.
j1_center_from_pcb_edge = 16.62;
j1_opening_width = 22.5;
j1_opening_bottom = 5.5;

mount_tab_length = 14;
mount_tab_width = 16;
mount_hole_diameter = 6.5;

gasket_width = 1.8;
gasket_depth = 1.0;

outer_length = inside_length + 2 * wall;
outer_width = inside_width + 2 * wall;
base_height = inside_height + floor_thickness;
pcb_edge_y = (outer_width - pcb_width) / 2;
j1_lid_relief_center_y = pcb_edge_y + j1_center_from_pcb_edge;
// The lid is printed exterior-face down and flipped about Y for assembly.
// Its printable relief therefore remains mirrored relative to the base notch.
j1_base_opening_center_y = outer_width - j1_lid_relief_center_y;

$fn = 48;

module rounded_box(size, radius) {
    hull() {
        for (x = [radius, size[0] - radius])
            for (y = [radius, size[1] - radius])
                translate([x, y, 0])
                    cylinder(r = radius, h = size[2]);
    }
}

module mounting_tab(y_center) {
    translate([-mount_tab_length, y_center - mount_tab_width / 2, 0])
        difference() {
            hull() {
                translate([mount_tab_length, 0, 0])
                    cube([1, mount_tab_width, floor_thickness]);
                translate([mount_tab_length / 2, mount_tab_width / 2, 0])
                    cylinder(d = mount_tab_width, h = floor_thickness);
            }
            translate([mount_tab_length / 2, mount_tab_width / 2, -0.1])
                cylinder(d = mount_hole_diameter,
                         h = floor_thickness + 0.2);
        }
}

module enclosure_screw_boss(x, y) {
    translate([x, y, floor_thickness - 0.1])
        difference() {
            cylinder(d = screw_boss_diameter, h = inside_height + 0.1);
            // Blind pocket entered from the top for a common M3 heat-set
            // insert.  Tune diameter/depth to the inserts actually used.
            translate([0, 0,
                       inside_height - lid_insert_depth])
                cylinder(d = lid_insert_hole_diameter,
                         h = lid_insert_depth + 0.3);
        }
}

module pcb_standoff(x, y) {
    translate([x, y, floor_thickness - 0.1])
        difference() {
            cylinder(d = 7, h = pcb_standoff_height + 0.1);
            translate([0, 0, -0.1])
                cylinder(d = pcb_screw_diameter,
                         h = pcb_standoff_height + 0.4);
        }
}

module base() {
    difference() {
        union() {
            difference() {
                rounded_box(
                    [outer_length, outer_width, base_height],
                    corner_radius
                );
                translate([wall, wall, floor_thickness])
                    rounded_box(
                        [inside_length, inside_width,
                         inside_height + 0.1],
                        max(corner_radius - wall, 1)
                    );
            }
            mounting_tab(outer_width / 2);
            translate([outer_length, outer_width, 0])
                rotate([0, 0, 180])
                    mounting_tab(outer_width / 2);

            for (x = [screw_edge_offset,
                      outer_length - screw_edge_offset])
                for (y = [screw_edge_offset,
                          outer_width - screw_edge_offset])
                    enclosure_screw_boss(x, y);

            for (x = [(outer_length - pcb_hole_spacing_x) / 2
                      + pcb_shift_x,
                      (outer_length + pcb_hole_spacing_x) / 2
                      + pcb_shift_x])
                for (y = [(outer_width - pcb_hole_spacing_y) / 2,
                          (outer_width + pcb_hole_spacing_y) / 2])
                    pcb_standoff(x, y);
        }

        // Direct-access notch for inserting the wire-side J1 plug through
        // the left wall.  It remains open at the top for support-free print.
        translate([-0.1,
                   j1_base_opening_center_y - j1_opening_width / 2,
                   j1_opening_bottom])
            cube([wall + 0.2,
                  j1_opening_width,
                  base_height - j1_opening_bottom + 0.2]);
    }
}

module lid() {
    lip_height = 3;
    lip_wall = 1.6;

    difference() {
        union() {
            rounded_box(
                [outer_length, outer_width, lid_thickness],
                corner_radius
            );
            translate([wall + lid_clearance,
                       wall + lid_clearance,
                       lid_thickness - 0.1])
                difference() {
                    rounded_box(
                        [inside_length - 2 * lid_clearance,
                         inside_width - 2 * lid_clearance,
                         lip_height + 0.1],
                        max(corner_radius - wall, 1)
                    );
                    translate([lip_wall, lip_wall, -0.1])
                        rounded_box(
                            [inside_length - 2 * lid_clearance
                             - 2 * lip_wall,
                             inside_width - 2 * lid_clearance
                             - 2 * lip_wall,
                             lip_height + 0.2],
                            max(corner_radius - wall - lip_wall, 0.8)
                        );
                }
        }

        for (x = [screw_edge_offset,
                  outer_length - screw_edge_offset])
            for (y = [screw_edge_offset,
                      outer_width - screw_edge_offset])
                translate([x, y, -0.1])
                    cylinder(d = lid_screw_clearance_diameter,
                             h = lid_thickness + lip_height + 0.2);

        // Remove the lid lip above J1 while retaining the solid lid roof.
        translate([-0.1,
                   j1_lid_relief_center_y - j1_opening_width / 2,
                   lid_thickness - 0.15])
            cube([wall + lid_clearance + lip_wall + 0.3,
                  j1_opening_width,
                  lip_height + 0.4]);

        // Shallow gasket channel on the underside.
        translate([wall / 2, wall / 2, lid_thickness - gasket_depth])
            difference() {
                rounded_box(
                    [outer_length - wall,
                     outer_width - wall,
                     gasket_depth + 0.1],
                    max(corner_radius - wall / 2, 1)
                );
                translate([gasket_width, gasket_width, -0.1])
                    rounded_box(
                        [outer_length - wall - 2 * gasket_width,
                         outer_width - wall - 2 * gasket_width,
                         gasket_depth + 0.3],
                        max(corner_radius - wall / 2
                            - gasket_width, 0.8)
                    );
            }
    }
}

if (part == "base") {
    base();
} else if (part == "lid") {
    lid();
} else {
    base();
    translate([0, outer_width + 12, 0])
        lid();
}
