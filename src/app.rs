use egui::{hex_color, Color32, Panel, Theme, Frame, Shadow, Margin, Ui, InnerResponse};

/// We derive Deserialize/Serialize so we can persist app state on shutdown.
#[derive(serde::Deserialize, serde::Serialize)]
#[serde(default)] // if we add new fields, give them default values when deserializing old state
pub struct PortfolioApp {
    // Example stuff:
    label: String,

    #[serde(skip)] // This how you opt-out of serialization of a field
    value: f32,
}

impl Default for PortfolioApp {
    fn default() -> Self {
        Self {
            // Example stuff:
            label: "Hello World!".to_owned(),
            value: 2.7,
        }
    }
}

impl PortfolioApp {
    /// Called once before the first frame.
    pub fn new(cc: &eframe::CreationContext<'_>) -> Self {
        // This is also where you can customize the look and feel of egui using
        // `cc.egui_ctx.set_visuals` and `cc.egui_ctx.set_fonts`.

        // Load previous app state (if any).
        // Note that you must enable the `persistence` feature for this to work.
        let app = if let Some(storage) = cc.storage {
            eframe::get_value(storage, eframe::APP_KEY).unwrap_or_default()
        } else {
            Default::default()
        };

        cc.egui_ctx.style_mut_of(Theme::Dark, |style| {
            style.visuals.extreme_bg_color = hex_color!("191e21");
            style.visuals.faint_bg_color = hex_color!("2f3b4b");
            style.visuals.panel_fill = hex_color!("1f2c3a");
            style.visuals.window_fill = style.visuals.extreme_bg_color;
        });

        app
    }
}

impl eframe::App for PortfolioApp {
    /// Called by the framework to save state before shutdown.
    fn save(&mut self, storage: &mut dyn eframe::Storage) {
        eframe::set_value(storage, eframe::APP_KEY, self);
    }

    /// Called each time the UI needs repainting, which may be many times per second.
    fn ui(&mut self, ui: &mut egui::Ui, _frame: &mut eframe::Frame) {
        Panel::top("top_panel")
            .show_separator_line(false)
            .frame(Frame::side_top_panel(ui.style())
                //.fill(ui.visuals().faint_bg_color)
                .shadow(Shadow {
                    offset: [0, 0],
                    blur: 16,
                    spread: 50,
                    color: Color32::BLACK,
                }))
            .show(ui, |ui| {
            // The top panel is often a good place for a menu bar:

            egui::MenuBar::new().ui(ui, |ui| {
                // NOTE: no File->Quit on web pages!
                let is_web = cfg!(target_arch = "wasm32");
                if !is_web {
                    ui.menu_button("File", |ui| {
                        if ui.button("Quit").clicked() {
                            ui.send_viewport_cmd(egui::ViewportCommand::Close);
                        }
                    });
                    ui.add_space(16.0);
                }

                egui::widgets::global_theme_preference_buttons(ui);
            });
        });

        let total_width = ui.available_width();
        let side_width = (((total_width - 800.0) / 2.0) - 100.0).max(0.0);
        Panel::left("left_space")
            .resizable(false)
            .exact_size(side_width)
            .show_separator_line(false)
            .frame(Frame::side_top_panel(ui.style()).fill(ui.visuals().extreme_bg_color))
            .show(ui, |_| {});
        Panel::right("right_space")
            .resizable(false)
            .exact_size(side_width)
            .show_separator_line(false)
            .frame(Frame::side_top_panel(ui.style()).fill(ui.visuals().extreme_bg_color))
            .show(ui, |_| {});

        egui::CentralPanel::default()
            .frame(Frame::central_panel(ui.style())
                .fill(ui.visuals().extreme_bg_color)
                .inner_margin(Margin::ZERO))
            .show(ui, |ui| {
                ContentSection::new()
                    .show(ui, |ui| {
                        // The central panel the region left after adding TopPanel's and SidePanel's
                        ui.heading("eframe template");

                        ui.horizontal(|ui| {
                            ui.label("Write something: ");
                            ui.text_edit_singleline(&mut self.label);
                        });

                        ui.add(egui::Slider::new(&mut self.value, 0.0..=10.0).text("value"));
                        if ui.button("Increment").clicked() {
                            self.value += 1.0;
                        }

                        ui.separator();

                        ui.add(egui::github_link_file!(
                            "https://github.com/emilk/eframe_template/blob/main/",
                            "Source code."
                        ));
                    });

                ui.with_layout(egui::Layout::bottom_up(egui::Align::LEFT), |ui| {
                    powered_by_egui_and_eframe(ui);
                    egui::warn_if_debug_build(ui);
                });
            });

    }
}

fn powered_by_egui_and_eframe(ui: &mut egui::Ui) {
    ui.horizontal(|ui| {
        ui.spacing_mut().item_spacing.x = 0.0;
        ui.label("Powered by ");
        ui.hyperlink_to("egui", "https://github.com/emilk/egui");
        ui.label(" and ");
        ui.hyperlink_to(
            "eframe",
            "https://github.com/emilk/egui/tree/master/crates/eframe",
        );
        ui.label(".");
    });
}

struct ContentSection {

}

impl ContentSection {
    pub fn new() -> Self {
        ContentSection {

        }
    }

    pub fn show<R>(
        self,
        ui: &mut Ui,
        add_contents: impl FnOnce(&mut Ui) -> R,
    ) -> InnerResponse<R> {
        let frame = Frame::central_panel(ui.style())
            .fill(ui.visuals().faint_bg_color)
            .shadow(Shadow {
                offset: [4, 6],
                blur: 12,
                spread: 1,
                color: hex_color!("010101"),
            })
            .outer_margin(Margin::symmetric(20, 15));

        frame.show(ui, add_contents)
    }
}