/*
  Preliminary auxiliary marker-lamp controller enclosure.
  Units: millimeters.

  Export base and lid separately by changing `part`.
*/

part = "assembly"; // "base", "lid", or "assembly"

inside_length = 90;
inside_width = 62;
inside_height = 30;
wall = 3;
floor_thickness = 3;
lid_thickness = 3;
corner_radius = 5;
lid_clearance = 0.30;

screw_diameter = 3.2;
screw_boss_diameter = 8;
screw_edge_offset = 8;

pcb_length = 72;
pcb_width = 48;
pcb_hole_spacing_x = 64;
pcb_hole_spacing_y = 40;
pcb_standoff_height = 5;
pcb_screw_diameter = 2.7;

cable_hole_diameter = 12.5;
cable_hole_spacing = 22;

mount_tab_length = 14;
mount_tab_width = 16;
mount_hole_diameter = 6.5;

gasket_width = 1.8;
gasket_depth = 1.0;

outer_length = inside_length + 2 * wall;
outer_width = inside_width + 2 * wall;
base_height = inside_height + floor_thickness;

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
            translate([0, 0, -0.1])
                cylinder(d = screw_diameter,
                         h = inside_height + 0.4);
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

            for (x = [(outer_length - pcb_hole_spacing_x) / 2,
                      (outer_length + pcb_hole_spacing_x) / 2])
                for (y = [(outer_width - pcb_hole_spacing_y) / 2,
                          (outer_width + pcb_hole_spacing_y) / 2])
                    pcb_standoff(x, y);
        }

        // Three provisional cable-gland holes on one short wall.
        for (y = [outer_width / 2 - cable_hole_spacing,
                  outer_width / 2,
                  outer_width / 2 + cable_hole_spacing])
            translate([-0.1, y, floor_thickness + inside_height / 2])
                rotate([0, 90, 0])
                    cylinder(d = cable_hole_diameter,
                             h = wall + 0.2);
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
                    cylinder(d = screw_diameter + 0.4,
                             h = lid_thickness + lip_height + 0.2);

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
