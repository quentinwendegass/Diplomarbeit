//
//  UIColor+CustomColors.swift
//  SIMplePhone
//
//  Created by Lukas Kuster on 10.01.19.
//  Copyright © 2019 Lukas Kuster. All rights reserved.
//

import UIKit

extension UIColor {
    static var random: UIColor {
        return UIColor(red: .random(in: 0...1),
                       green: .random(in: 0...1),
                       blue: .random(in: 0...1),
                       alpha: 1.0)
    }
    
    static var iosGreen: UIColor {
        return UIColor(red: 0.30, green: 0.85, blue: 0.39, alpha: 1.0)
    }
    
    static var lighterGray: UIColor {
        return UIColor(red: 0.83, green: 0.83, blue: 0.84, alpha: 1.0)
    }
    
    static var cellSeperatorGray: UIColor {
        return UIColor(red: 0.78, green: 0.78, blue: 0.80, alpha: 1.0)
    }
    
    static var tableViewBackground: UIColor {
        return UIColor(red:0.94, green: 0.94, blue: 0.96, alpha: 1.0)
    }
}
