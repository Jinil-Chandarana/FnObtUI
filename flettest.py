import datetime
import flet as ft

current_time = datetime.datetime.now()

def main(page: ft.Page):
    # global start_sel_date
    page.title = "Trading Parameters"
    page.padding = 30
    page.vertical_alignment = "top"
    page.horizontal_alignment = "center"
    page.theme_mode = 'light'

    start_date_tx = ft.Text("No start date selected", size=16)
    end_date_tx = ft.Text("No end date selected", size=16)
    start_time_tx = ft.Text("No start time selected", size=16)
    end_time_tx = ft.Text("No end time selected", size=16)
    start_sel_time = None
    end_sel_time = None

    max_end_time = datetime.time(15, 29, 59)
    min_start_time = datetime.time(9, 15, 0)


    start_sel_date = None  # Store the selected start date
    end_sel_date = None  # Store the selected end date
    
    def start_dt_handle_change(e):
        nonlocal start_sel_date    
        start_sel_date = (e.control.value).date()
        start_date_tx.value = f"{e.control.value.date()}"
        page.update()
    
    def end_dt_handle_change(e):
        nonlocal end_sel_date
        end_sel_date = (e.control.value).date()
        end_date_tx.value = f"{end_sel_date}"
        page.update()

    def start_time_handle_change(e):
        nonlocal start_sel_time
        if e.control.value < min_start_time:
            page.add(ft.Text("Start time cannot be earlier than 09:15:00!", color="red"))
        else:
            start_sel_time = (e.control.value)
            start_time_tx.value = f"{start_sel_time}"
        page.update()


    def end_time_handle_change(e):
        nonlocal end_sel_time
        if start_sel_time and e.control.value <= start_sel_time:
            page.add(ft.Text("End time must be greater than start time!", color="red"))
        elif e.control.value > max_end_time:
            page.add(ft.Text("End time cannot exceed 15:29:59!", color="red"))
        else:
            end_sel_time = e.control.value
            end_time_tx.value = f"{end_sel_time}"
        page.update()


    def handle_dismissal(e):
        page.add(ft.Text(f"DatePicker dismissed"))

    def handle_start_time_change(e):
        page.add(ft.Text(f"TimePicker change: {start_time.value}"))
    
    def handle_end_time_change(e):
        page.add(ft.Text(f"TimePicker change: {end_time.value}"))
    
    def handle_entry_mode_change(e):
        page.add(ft.Text(f"TimePicker Entry mode changed to {e.entry_mode}"))


    def open_end_date_picker(e):
        if start_sel_date is None:
            page.add(ft.Text("Please select a start date first!", color="red"))
        else:
            page.open(
                ft.DatePicker(
                    first_date=start_sel_date,  # Restrict selection to after start date
                    last_date=datetime.datetime(
                        year=current_time.year, month=current_time.month, day=current_time.day
                    ),
                    on_change=end_dt_handle_change,
                    on_dismiss=handle_dismissal,
                )
            )

    start_time = ft.TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        on_change=start_time_handle_change,
        on_dismiss=handle_dismissal,
        on_entry_mode_change=handle_entry_mode_change,
    )

    end_time = ft.TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        on_change=end_time_handle_change,
        on_dismiss=handle_dismissal,
        on_entry_mode_change=handle_entry_mode_change,
    )
    strike_gap = ft.TextField(label="Symbol Strike Gap", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    ce_strike_difference = ft.TextField(label="CE ATM Difference", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    multi_ui = ft.TextField(label="Multiplier", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    pe_strike_difference = ft.TextField(label="PE ATM Difference", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    lot_size = ft.TextField(label="Lot Size", keyboard_type=ft.KeyboardType.NUMBER, width=200)
    margin = ft.TextField(label="Estimated Margin", keyboard_type=ft.KeyboardType.NUMBER, width=200)

    entry_action = ft.Dropdown(
        label="Entry Action",
        options=[ft.dropdown.Option("Buy"), ft.dropdown.Option("Sell")],
        width=200
    )
    expiry_ui = ft.Dropdown(
        label="Expiry",
        options=[ft.dropdown.Option("weekly"), ft.dropdown.Option("next weekly"), ft.dropdown.Option("monthly")],
        width=200
    )

    # Target controls
    target_check = ft.Checkbox(label="Target")
    target_value = ft.TextField(label="Target Value", keyboard_type=ft.KeyboardType.NUMBER, visible=False, width=150)
    target_type = ft.Dropdown(
        options=[ft.dropdown.Option("ABS"), ft.dropdown.Option("%")],
        visible=False,
        width=100
    )
    # Handle target checkbox change
    def target_changed(e):
        target_value.visible = target_check.value
        target_type.visible = target_check.value
        page.update()

    target_check.on_change = target_changed

    # Create form controls
    symbol = ft.TextField(label="Symbol", width=200)


    #Hnadle SL checkbox change
    sl_check = ft.Checkbox(label="SL")
    sl_value = ft.TextField(label="SL Value", keyboard_type=ft.KeyboardType.NUMBER, visible=False, width=150)
    sl_type = ft.Dropdown(
        options=[ft.dropdown.Option("ABS"), ft.dropdown.Option("%")],
        visible=False,
        width=100
    )

    def sl_changed(e):
        sl_value.visible = sl_check.value
        sl_type.visible = sl_check.value
        page.update()
    sl_check.on_change = sl_changed
    
    def submit_clicked(e):
        if start_time.value>end_time.value:
            print("time error")
        else:
            output = {
                "symbol": symbol.value,
                "start_date": start_sel_date,
                "end_date": end_sel_date,
                "start_time": start_time.value,
                "end_time": end_time.value,
                "strike_gap": int(strike_gap.value) if strike_gap.value else 0,
                "ce_atm_difference": int(ce_strike_difference.value) if ce_strike_difference.value else 0,
                "pe_atm_difference": int(pe_strike_difference.value) if pe_strike_difference.value else 0,
                "lot_size": int(lot_size.value) if lot_size.value else 0,
                "margin": float(margin.value) if margin.value else 0.0,
                "entry_action": entry_action.value,
                "expiry": expiry_ui.value,
                "target_enabled": target_check.value,
                "target_value": float(target_value.value) if target_check.value and target_value.value else None,
                "target_type": target_type.value if target_check.value else None,
                "sl_enabled": sl_check.value,
                "sl_value": float(sl_value.value) if sl_check.value and sl_value.value else None,
                "sl_type": sl_type.value if sl_check.value else None,
            }
            print("Form submitted:", output)
    # Build the form
    page.add(
        ft.Row([
            ft.Column([
            ft.Row([symbol], alignment="center"),
            ft.Row([
                ft.Column([
                    # ft.Text("Start Date:"),
                    ft.Row([
                        ft.ElevatedButton
                        (
                            "start date",
                            icon=ft.Icons.CALENDAR_MONTH,
                            on_click=lambda _:  page.open(
                                ft.DatePicker(
                                first_date=datetime.datetime(year=1900, day=1, month=1),
                                last_date=datetime.datetime(year=current_time.year, month=current_time.month, day=current_time.day),
                                on_change=start_dt_handle_change,
                                on_dismiss=handle_dismissal,
                                )
                            )
                        ),
                        start_date_tx,
                   
                    ]),
                    ft.Row([ft.ElevatedButton
                        (
                            "end Date",
                            icon=ft.icons.CALENDAR_MONTH,
                            on_click=open_end_date_picker
                        ),
                        end_date_tx,]),

                    ft.Row([
                        ft.ElevatedButton
                        (
                            "start Time",
                            icon=ft.icons.ACCESS_TIME,
                            on_click=lambda _: page.open(start_time),
                        ),
                        start_time_tx,
                    ]),
                    ft.Row([
                        ft.ElevatedButton
                        (
                                "end Time",
                                icon=ft.icons.ACCESS_TIME,
                                on_click=lambda _: page.open(end_time),
                        ), 
                        end_time_tx
                    ]),
                    
                ], alignment="center"),

             
            ],alignment="center"),
            ft.Row([strike_gap], alignment="center"),
            ft.Row([lot_size], alignment="center"),
            ft.Row([margin], alignment="center"),
            ft.Row([entry_action], alignment="center"),
          
            ft.ElevatedButton("Submit", on_click=submit_clicked)
        ], spacing=20, alignment="left"),
        ft.Column([
            ft.Row([ce_strike_difference], alignment="center"),
            ft.Row([pe_strike_difference], alignment ="center"),
            ft.Row([multi_ui], alignment="center"),
            ft.Row([expiry_ui], alignment="center"),
            ft.Row([
                target_check,
                ft.Container(target_value, padding=5),
                ft.Container(target_type, padding=5)
                 ], alignment="center"),
            ft.Row([
                sl_check,
                ft.Container(sl_value, padding=5),
                ft.Container(sl_type, padding=5)
                 ], alignment="center"),     
        ], spacing=20, alignment="center" )
        ], alignment="top")
       
        
    )

ft.app(main)