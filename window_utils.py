def switch_to_popup(driver, wait, main_window):
    all_windows = driver.window_handles

    main_window = driver.current_window_handle
    wait.until(lambda d: len(d.window_handles) > 1)
    popup_window = [w for w in all_windows if w != main_window][0]

    driver.switch_to.window(popup_window)
    return popup_window